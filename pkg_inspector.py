import os
from typing import Optional

from pkginfo import UnpackedSDist


class PackageInspector:
    """Class to encapsulate inspection tools with access to the package path."""
    def __init__(self, package_path: str):
        self.package_path = package_path

    def inspect_metadata(self) -> str:
        """Inspects package metadata for anomalies."""
        try:
            dist = UnpackedSDist(self.package_path)
            metadata = {
                "name": dist.name or "Unknown",
                "version": dist.version or "Unknown",
                "author": dist.author or "Unknown",
                "author_email": dist.author_email or "Unknown",
                "url": dist.url or "None",
                "description": dist.description or "None"
            }
            return str(metadata)
        except Exception as e:
            return f"Error extracting metadata: {str(e)}"

    def inspect_setup_py(self) -> str:
        """Reads the setup.py file content."""
        setup_py_path = os.path.join(self.package_path, 'setup.py')
        try:
            if os.path.exists(setup_py_path):
                with open(setup_py_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Truncate if too long to respect LLM token limits
                if len(content) > 2000:
                    return content[:2000] + "\n[Content truncated due to length]"
                return content
            return "setup.py not found"
        except Exception as e:
            return f"Error reading setup.py: {str(e)}"

    def inspect_init_py(self) -> str:
        """Reads the __init__.py file content from the package directory."""
        try:
            dist = UnpackedSDist(self.package_path)
            package_name = dist.name
            if not package_name:
                return "Could not determine package name from metadata"
            package_dir = self._find_package_dir(package_name)
            if not package_dir:
                return "Package directory not found"
            init_py_path = os.path.join(package_dir, '__init__.py')
            if os.path.exists(init_py_path):
                with open(init_py_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Truncate if too long
                if len(content) > 2000:
                    return content[:2000] + "\n[Content truncated due to length]"
                return content
            return "__init__.py not found"
        except Exception as e:
            return f"Error inspecting __init__.py: {str(e)}"

    def inspect_project_structure(self) -> str:
        """Lists the package's directory structure."""
        try:
            structure = []
            for root, dirs, files in os.walk(self.package_path):
                level = root.replace(self.package_path, '').count(os.sep)
                indent = ' ' * 4 * level
                structure.append(f"{indent}{os.path.basename(root)}/")
                sub_indent = ' ' * 4 * (level + 1)
                for f in files:
                    structure.append(f"{sub_indent}{f}")
            return '\n'.join(structure) or "No files or directories found"
        except Exception as e:
            return f"Error inspecting project structure: {str(e)}"

    def _find_package_dir(self, package_name: str) -> Optional[str]:
        """Helper to find the package directory based on package name."""
        for root, dirs, files in os.walk(self.package_path):
            if package_name in dirs:
                return os.path.join(root, package_name)
        return None

if __name__ == "__main__":

    package_path = "0.2/src/libida-0.2"  # Update this path if needed

    # Create an instance of PackageInspector
    inspector = PackageInspector(package_path)

    # Test inspect_metadata
    print("Testing inspect_metadata:")
    metadata_result = inspector.inspect_metadata()
    print(metadata_result)
    print("-" * 40)

    # Test inspect_setup_py
    print("Testing inspect_setup_py:")
    setup_py_result = inspector.inspect_setup_py()
    print(setup_py_result)
    print("-" * 40)

    # Test inspect_init_py
    print("Testing inspect_init_py:")
    init_py_result = inspector.inspect_init_py()
    print(init_py_result)
    print("-" * 40)

    # Test inspect_project_structure
    print("Testing inspect_project_structure:")
    project_structure_result = inspector.inspect_project_structure()
    print(project_structure_result)
    print("-" * 40)
