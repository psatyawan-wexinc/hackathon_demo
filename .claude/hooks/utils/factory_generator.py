#!/usr/bin/env python3
"""
Factory Boy generator utility for Claude Code Hooks

Automatically generates Factory Boy factory definitions for SQLAlchemy models
and other data structures.
"""

import ast
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ModelParser:
    """Parse Python files to extract model definitions."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.models = []
        
    def parse_file(self) -> List[Dict]:
        """
        Parse the file and extract model definitions.
        
        Returns:
            List of model dictionaries with fields and metadata
        """
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    model_info = self._parse_class(node, content)
                    if model_info and self._is_model_class(model_info):
                        self.models.append(model_info)
            
            return self.models
            
        except Exception as e:
            print(f"Error parsing file {self.file_path}: {str(e)}")
            return []
    
    def _parse_class(self, node: ast.ClassDef, content: str) -> Dict:
        """Parse a class definition and extract field information."""
        model_info = {
            "name": node.name,
            "base_classes": [self._get_name(base) for base in node.bases],
            "fields": [],
            "imports": self._extract_imports(content),
            "is_sqlalchemy": False,
            "is_pydantic": False,
            "table_name": None
        }
        
        # Check if it's a SQLAlchemy or Pydantic model
        base_classes = model_info["base_classes"]
        model_info["is_sqlalchemy"] = any(base in ["Base", "Model", "db.Model"] for base in base_classes)
        model_info["is_pydantic"] = any(base in ["BaseModel", "pydantic.BaseModel"] for base in base_classes)
        
        # Parse fields
        for item in node.body:
            if isinstance(item, ast.Assign):
                field_info = self._parse_field(item)
                if field_info:
                    model_info["fields"].append(field_info)
            elif isinstance(item, ast.AnnAssign):
                field_info = self._parse_annotated_field(item)
                if field_info:
                    model_info["fields"].append(field_info)
        
        # Extract table name for SQLAlchemy models
        model_info["table_name"] = self._extract_table_name(node)
        
        return model_info
    
    def _parse_field(self, node: ast.Assign) -> Optional[Dict]:
        """Parse a regular field assignment."""
        if not node.targets or not isinstance(node.targets[0], ast.Name):
            return None
        
        field_name = node.targets[0].id
        field_type = self._infer_type_from_value(node.value)
        
        return {
            "name": field_name,
            "type": field_type,
            "nullable": self._is_nullable(node.value),
            "primary_key": self._is_primary_key(node.value),
            "foreign_key": self._is_foreign_key(node.value),
            "unique": self._is_unique(node.value),
            "default": self._extract_default(node.value)
        }
    
    def _parse_annotated_field(self, node: ast.AnnAssign) -> Optional[Dict]:
        """Parse an annotated field assignment."""
        if not isinstance(node.target, ast.Name):
            return None
        
        field_name = node.target.id
        field_type = self._get_type_annotation(node.annotation)
        
        return {
            "name": field_name,
            "type": field_type,
            "nullable": "Optional" in field_type or "None" in field_type,
            "primary_key": False,
            "foreign_key": False,
            "unique": False,
            "default": self._extract_default(node.value) if node.value else None
        }
    
    def _get_name(self, node) -> str:
        """Get the name of an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        else:
            return "Unknown"
    
    def _get_type_annotation(self, node) -> str:
        """Get the type annotation as a string."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
        else:
            return "Any"
    
    def _infer_type_from_value(self, node) -> str:
        """Infer the field type from its value (SQLAlchemy Column, etc.)."""
        if isinstance(node, ast.Call):
            func_name = self._get_name(node.func)
            if "Column" in func_name:
                if node.args:
                    return self._get_name(node.args[0])
            elif "relationship" in func_name:
                return "relationship"
        return "Unknown"
    
    def _is_nullable(self, node) -> bool:
        """Check if a field is nullable."""
        if isinstance(node, ast.Call) and "Column" in self._get_name(node.func):
            for keyword in node.keywords:
                if keyword.arg == "nullable":
                    return keyword.value.value if isinstance(keyword.value, ast.Constant) else True
        return True
    
    def _is_primary_key(self, node) -> bool:
        """Check if a field is a primary key."""
        if isinstance(node, ast.Call) and "Column" in self._get_name(node.func):
            for keyword in node.keywords:
                if keyword.arg == "primary_key":
                    return keyword.value.value if isinstance(keyword.value, ast.Constant) else False
        return False
    
    def _is_foreign_key(self, node) -> bool:
        """Check if a field is a foreign key."""
        if isinstance(node, ast.Call) and "Column" in self._get_name(node.func):
            for arg in node.args:
                if isinstance(arg, ast.Call) and "ForeignKey" in self._get_name(arg.func):
                    return True
        return False
    
    def _is_unique(self, node) -> bool:
        """Check if a field is unique."""
        if isinstance(node, ast.Call) and "Column" in self._get_name(node.func):
            for keyword in node.keywords:
                if keyword.arg == "unique":
                    return keyword.value.value if isinstance(keyword.value, ast.Constant) else False
        return False
    
    def _extract_default(self, node) -> Optional[str]:
        """Extract default value from a field."""
        if isinstance(node, ast.Call) and "Column" in self._get_name(node.func):
            for keyword in node.keywords:
                if keyword.arg == "default":
                    if isinstance(keyword.value, ast.Constant):
                        return repr(keyword.value.value)
                    else:
                        return self._get_name(keyword.value)
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        return None
    
    def _extract_table_name(self, node: ast.ClassDef) -> Optional[str]:
        """Extract table name from SQLAlchemy model."""
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "__tablename__":
                        if isinstance(item.value, ast.Constant):
                            return item.value.value
        return None
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from file content."""
        imports = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        return imports
    
    def _is_model_class(self, model_info: Dict) -> bool:
        """Check if a class is likely a data model."""
        base_classes = model_info["base_classes"]
        
        # SQLAlchemy models
        if any(base in ["Base", "Model", "db.Model"] for base in base_classes):
            return True
        
        # Pydantic models
        if any(base in ["BaseModel", "pydantic.BaseModel"] for base in base_classes):
            return True
        
        # Check for common model patterns
        if model_info["table_name"] or len(model_info["fields"]) > 2:
            return True
        
        return False


class FactoryGenerator:
    """Generate Factory Boy factory definitions for models."""
    
    def __init__(self, model_info: Dict):
        self.model_info = model_info
        
    def generate_factory(self) -> str:
        """
        Generate a Factory Boy factory definition.
        
        Returns:
            String containing the factory definition
        """
        model_name = self.model_info["name"]
        factory_name = f"{model_name}Factory"
        
        # Start building the factory
        factory_lines = []
        factory_lines.append(f"class {factory_name}(factory.Factory):")
        factory_lines.append("    class Meta:")
        
        if self.model_info["is_sqlalchemy"]:
            factory_lines.append(f"        model = {model_name}")
            factory_lines.append("        sqlalchemy_session = Session")
            factory_lines.append("        sqlalchemy_session_persistence = 'commit'")
        else:
            factory_lines.append(f"        model = {model_name}")
        
        factory_lines.append("")
        
        # Generate field definitions
        for field in self.model_info["fields"]:
            field_def = self._generate_field_definition(field)
            if field_def:
                factory_lines.append(f"    {field_def}")
        
        # Add traits for common scenarios
        traits = self._generate_traits()
        if traits:
            factory_lines.append("")
            factory_lines.append("    class Params:")
            for trait in traits:
                factory_lines.append(f"        {trait}")
        
        return "\n".join(factory_lines)
    
    def _generate_field_definition(self, field: Dict) -> Optional[str]:
        """Generate a field definition for the factory."""
        field_name = field["name"]
        field_type = field["type"]
        
        # Skip primary keys and relationships
        if field["primary_key"] or field_type == "relationship":
            return None
        
        # Generate appropriate factory definition based on type
        if "Integer" in field_type or "int" in field_type:
            return f"{field_name} = factory.Sequence(lambda n: n + 1)"
        elif "String" in field_type or "str" in field_type:
            if "email" in field_name.lower():
                return f"{field_name} = factory.Faker('email')"
            elif "name" in field_name.lower():
                return f"{field_name} = factory.Faker('name')"
            elif "phone" in field_name.lower():
                return f"{field_name} = factory.Faker('phone_number')"
            elif "address" in field_name.lower():
                return f"{field_name} = factory.Faker('address')"
            else:
                return f"{field_name} = factory.Faker('text', max_nb_chars=50)"
        elif "Boolean" in field_type or "bool" in field_type:
            return f"{field_name} = factory.Faker('boolean')"
        elif "DateTime" in field_type or "datetime" in field_type:
            return f"{field_name} = factory.Faker('date_time')"
        elif "Date" in field_type or "date" in field_type:
            return f"{field_name} = factory.Faker('date')"
        elif "Float" in field_type or "Numeric" in field_type or "float" in field_type:
            return f"{field_name} = factory.Faker('pyfloat', positive=True, max_value=1000)"
        elif "Text" in field_type:
            return f"{field_name} = factory.Faker('text')"
        else:
            # Default to text for unknown types
            return f"{field_name} = factory.Faker('text', max_nb_chars=20)"
    
    def _generate_traits(self) -> List[str]:
        """Generate trait definitions for common scenarios."""
        traits = []
        
        # Look for boolean fields that could have traits
        boolean_fields = [f for f in self.model_info["fields"] if "Boolean" in f["type"] or "bool" in f["type"]]
        
        for field in boolean_fields:
            field_name = field["name"]
            if "active" in field_name.lower():
                traits.append(f"inactive = factory.Trait({field_name}=False)")
            elif "enabled" in field_name.lower():
                traits.append(f"disabled = factory.Trait({field_name}=False)")
            elif "verified" in field_name.lower():
                traits.append(f"unverified = factory.Trait({field_name}=False)")
        
        return traits
    
    def generate_imports(self) -> str:
        """Generate necessary import statements for the factory."""
        imports = [
            "import factory",
            "from factory import Faker, Sequence, Trait",
            "from datetime import datetime, date"
        ]
        
        # Add SQLAlchemy imports if needed
        if self.model_info["is_sqlalchemy"]:
            imports.append("from sqlalchemy.orm import Session")
        
        # Add model import
        model_name = self.model_info["name"]
        imports.append(f"from src.models import {model_name}")
        
        return "\n".join(imports)


def generate_factory_file(model_file: str, output_file: str = None) -> bool:
    """
    Generate a Factory Boy factory file for models in the given file.
    
    Args:
        model_file: Path to the file containing model definitions
        output_file: Path to output the factory file (optional)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Parse the model file
        parser = ModelParser(model_file)
        models = parser.parse_file()
        
        if not models:
            print(f"No models found in {model_file}")
            return False
        
        # Determine output file
        if output_file is None:
            model_path = Path(model_file)
            if "models" in model_path.parts:
                # Replace models with test_utils/factories
                parts = list(model_path.parts)
                models_index = parts.index("models")
                parts[models_index] = "test_utils"
                parts.insert(models_index + 1, "factories")
                output_path = Path(*parts)
                output_file = str(output_path.with_name(f"factory_{output_path.stem}.py"))
            else:
                output_file = str(model_path.with_name(f"factory_{model_path.stem}.py"))
        
        # Generate factory content
        content_lines = []
        
        # Generate imports (combine from all models)
        all_imports = set()
        for model in models:
            generator = FactoryGenerator(model)
            imports = generator.generate_imports()
            for imp in imports.split('\n'):
                all_imports.add(imp)
        
        content_lines.extend(sorted(all_imports))
        content_lines.append("")
        content_lines.append("")
        
        # Generate factories
        for model in models:
            generator = FactoryGenerator(model)
            factory_code = generator.generate_factory()
            content_lines.append(factory_code)
            content_lines.append("")
            content_lines.append("")
        
        # Write the file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write("\n".join(content_lines))
        
        print(f"Generated factory file: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating factory file: {str(e)}")
        return False