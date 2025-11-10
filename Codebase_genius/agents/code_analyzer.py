"""
Code Analyzer Agent - Performs deep code analysis and builds Code Context Graphs.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
import networkx as nx
import tree_sitter
from tree_sitter import Language, Parser, Node


@dataclass
class CodeElement:
    """Represents a code element (function, class, variable, etc.)."""
    name: str
    type: str  # 'function', 'class', 'variable', 'import', 'module'
    file_path: str
    line_start: int
    line_end: int
    column_start: int
    column_end: int
    docstring: Optional[str] = None
    parameters: Optional[List[str]] = None
    return_type: Optional[str] = None
    parent: Optional[str] = None
    children: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class CodeContextGraph:
    """Code Context Graph containing relationships between code elements."""
    elements: Dict[str, CodeElement]
    relationships: List[Tuple[str, str, str]]  # (from, to, relationship_type)
    graph: nx.DiGraph
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'elements': {k: v.to_dict() for k, v in self.elements.items()},
            'relationships': self.relationships,
            'graph_nodes': list(self.graph.nodes()),
            'graph_edges': list(self.graph.edges())
        }


class CodeAnalyzer:
    """Analyzes code and builds Code Context Graphs."""
    
    def __init__(self):
        self.parsers = {}
        self.language_files = {
            'python': 'tree-sitter-python',
            'javascript': 'tree-sitter-javascript',
            'java': 'tree-sitter-java',
            'cpp': 'tree-sitter-cpp',
            'rust': 'tree-sitter-rust',
            'go': 'tree-sitter-go'
        }
        self._initialize_parsers()
    
    def _initialize_parsers(self):
        """Initialize Tree-sitter parsers for different languages."""
        try:
            # Python parser
            if 'python' in self.language_files:
                PY_LANGUAGE = Language('build/my-languages.so', 'python')
                self.parsers['python'] = Parser(PY_LANGUAGE)
            
            # JavaScript parser
            if 'javascript' in self.language_files:
                JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
                self.parsers['javascript'] = Parser(JS_LANGUAGE)
            
            # Java parser
            if 'java' in self.language_files:
                JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
                self.parsers['java'] = Parser(JAVA_LANGUAGE)
            
            # C++ parser
            if 'cpp' in self.language_files:
                CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')
                self.parsers['cpp'] = Parser(CPP_LANGUAGE)
            
            # Rust parser
            if 'rust' in self.language_files:
                RUST_LANGUAGE = Language('build/my-languages.so', 'rust')
                self.parsers['rust'] = Parser(RUST_LANGUAGE)
            
            # Go parser
            if 'go' in self.language_files:
                GO_LANGUAGE = Language('build/my-languages.so', 'go')
                self.parsers['go'] = Parser(GO_LANGUAGE)
                
        except Exception as e:
            print(f"Warning: Could not initialize Tree-sitter parsers: {e}")
            print("Falling back to regex-based analysis")
    
    def analyze_codebase(self, repo_path: str, language: str, entry_points: List[str]) -> CodeContextGraph:
        """
        Analyze a codebase and build a Code Context Graph.
        
        Args:
            repo_path: Path to the repository
            language: Primary programming language
            entry_points: List of entry point files to analyze first
            
        Returns:
            CodeContextGraph object
        """
        repo_path = Path(repo_path)
        elements = {}
        relationships = []
        
        # Create NetworkX graph
        graph = nx.DiGraph()
        
        # Analyze entry points first
        for entry_point in entry_points:
            file_path = repo_path / entry_point
            if file_path.exists():
                file_elements, file_relationships = self._analyze_file(
                    file_path, language, str(repo_path)
                )
                elements.update(file_elements)
                relationships.extend(file_relationships)
        
        # Analyze remaining files
        for file_path in self._get_code_files(repo_path, language):
            if str(file_path.relative_to(repo_path)) not in entry_points:
                file_elements, file_relationships = self._analyze_file(
                    file_path, language, str(repo_path)
                )
                elements.update(file_elements)
                relationships.extend(file_relationships)
        
        # Build relationships in the graph
        for element_id, element in elements.items():
            graph.add_node(element_id, **element.to_dict())
        
        for from_id, to_id, rel_type in relationships:
            graph.add_edge(from_id, to_id, relationship=rel_type)
        
        return CodeContextGraph(
            elements=elements,
            relationships=relationships,
            graph=graph
        )
    
    def _analyze_file(self, file_path: Path, language: str, repo_root: str) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Analyze a single file and extract code elements."""
        elements = {}
        relationships = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return elements, relationships
        
        relative_path = str(file_path.relative_to(Path(repo_root)))
        
        if language in self.parsers:
            # Use Tree-sitter parser
            elements, relationships = self._parse_with_treesitter(
                content, relative_path, language
            )
        else:
            # Fall back to regex-based parsing
            elements, relationships = self._parse_with_regex(
                content, relative_path, language
            )
        
        return elements, relationships
    
    def _parse_with_treesitter(self, content: str, file_path: str, language: str) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Parse file using Tree-sitter."""
        elements = {}
        relationships = []
        
        try:
            parser = self.parsers[language]
            tree = parser.parse(bytes(content, 'utf8'))
            root_node = tree.root_node
            
            # Language-specific parsing
            if language == 'python':
                elements, relationships = self._parse_python_ast(root_node, file_path, content)
            elif language == 'javascript':
                elements, relationships = self._parse_javascript_ast(root_node, file_path, content)
            elif language == 'java':
                elements, relationships = self._parse_java_ast(root_node, file_path, content)
            # Add more languages as needed
            
        except Exception as e:
            print(f"Error parsing {file_path} with Tree-sitter: {e}")
            # Fall back to regex parsing
            return self._parse_with_regex(content, file_path, language)
        
        return elements, relationships
    
    def _parse_python_ast(self, root_node: Node, file_path: str, content: str) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Parse Python AST using Tree-sitter."""
        elements = {}
        relationships = []
        lines = content.split('\n')
        
        def traverse_node(node: Node, parent: Optional[str] = None):
            if node.type == 'function_definition':
                name = self._get_node_text(node, content, 'identifier')
                if name:
                    element = CodeElement(
                        name=name,
                        type='function',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1],
                        parent=parent
                    )
                    element_id = f"{file_path}:{name}"
                    elements[element_id] = element
                    
                    if parent:
                        relationships.append((parent, element_id, 'contains'))
                    
                    # Find function calls within this function
                    self._find_function_calls(node, content, element_id, elements, relationships, file_path)
            
            elif node.type == 'class_definition':
                name = self._get_node_text(node, content, 'identifier')
                if name:
                    element = CodeElement(
                        name=name,
                        type='class',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1],
                        parent=parent
                    )
                    element_id = f"{file_path}:{name}"
                    elements[element_id] = element
                    
                    if parent:
                        relationships.append((parent, element_id, 'contains'))
                    
                    # Traverse class methods
                    for child in node.children:
                        if child.type == 'block':
                            for grandchild in child.children:
                                traverse_node(grandchild, element_id)
            
            elif node.type == 'import_statement':
                # Handle imports
                module_name = self._get_import_name(node, content)
                if module_name:
                    element = CodeElement(
                        name=module_name,
                        type='import',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1]
                    )
                    element_id = f"{file_path}:import:{module_name}"
                    elements[element_id] = element
            
            # Traverse children
            for child in node.children:
                traverse_node(child, parent)
        
        traverse_node(root_node)
        return elements, relationships
    
    def _parse_javascript_ast(self, root_node: Node, file_path: str, content: str) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Parse JavaScript AST using Tree-sitter."""
        elements = {}
        relationships = []
        
        def traverse_node(node: Node, parent: Optional[str] = None):
            if node.type == 'function_declaration':
                name = self._get_node_text(node, content, 'identifier')
                if name:
                    element = CodeElement(
                        name=name,
                        type='function',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1],
                        parent=parent
                    )
                    element_id = f"{file_path}:{name}"
                    elements[element_id] = element
                    
                    if parent:
                        relationships.append((parent, element_id, 'contains'))
            
            elif node.type == 'class_declaration':
                name = self._get_node_text(node, content, 'identifier')
                if name:
                    element = CodeElement(
                        name=name,
                        type='class',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1],
                        parent=parent
                    )
                    element_id = f"{file_path}:{name}"
                    elements[element_id] = element
                    
                    if parent:
                        relationships.append((parent, element_id, 'contains'))
            
            # Traverse children
            for child in node.children:
                traverse_node(child, parent)
        
        traverse_node(root_node)
        return elements, relationships
    
    def _parse_java_ast(self, root_node: Node, file_path: str, content: str) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Parse Java AST using Tree-sitter."""
        elements = {}
        relationships = []
        
        def traverse_node(node: Node, parent: Optional[str] = None):
            if node.type == 'method_declaration':
                name = self._get_node_text(node, content, 'identifier')
                if name:
                    element = CodeElement(
                        name=name,
                        type='function',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1],
                        parent=parent
                    )
                    element_id = f"{file_path}:{name}"
                    elements[element_id] = element
                    
                    if parent:
                        relationships.append((parent, element_id, 'contains'))
            
            elif node.type == 'class_declaration':
                name = self._get_node_text(node, content, 'identifier')
                if name:
                    element = CodeElement(
                        name=name,
                        type='class',
                        file_path=file_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        column_start=node.start_point[1],
                        column_end=node.end_point[1],
                        parent=parent
                    )
                    element_id = f"{file_path}:{name}"
                    elements[element_id] = element
                    
                    if parent:
                        relationships.append((parent, element_id, 'contains'))
                    
                    # Traverse class methods
                    for child in node.children:
                        if child.type == 'class_body':
                            for grandchild in child.children:
                                traverse_node(grandchild, element_id)
            
            # Traverse children
            for child in node.children:
                traverse_node(child, parent)
        
        traverse_node(root_node)
        return elements, relationships
    
    def _parse_with_regex(self, content: str, file_path: str, language: str) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Fallback regex-based parsing."""
        elements = {}
        relationships = []
        lines = content.split('\n')
        
        if language == 'python':
            elements, relationships = self._regex_parse_python(content, file_path, lines)
        elif language == 'javascript':
            elements, relationships = self._regex_parse_javascript(content, file_path, lines)
        elif language == 'java':
            elements, relationships = self._regex_parse_java(content, file_path, lines)
        # Add more languages as needed
        
        return elements, relationships
    
    def _regex_parse_python(self, content: str, file_path: str, lines: List[str]) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Regex-based Python parsing."""
        elements = {}
        relationships = []
        
        import re
        
        # Find functions
        func_pattern = r'^def\s+(\w+)\s*\([^)]*\):'
        for match in re.finditer(func_pattern, content, re.MULTILINE):
            name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type='function',
                file_path=file_path,
                line_start=line_num,
                line_end=line_num,
                column_start=match.start() - content.rfind('\n', 0, match.start()) - 1,
                column_end=match.end() - content.rfind('\n', 0, match.start()) - 1
            )
            element_id = f"{file_path}:{name}"
            elements[element_id] = element
        
        # Find classes
        class_pattern = r'^class\s+(\w+)(?:\([^)]*\))?:'
        for match in re.finditer(class_pattern, content, re.MULTILINE):
            name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type='class',
                file_path=file_path,
                line_start=line_num,
                line_end=line_num,
                column_start=match.start() - content.rfind('\n', 0, match.start()) - 1,
                column_end=match.end() - content.rfind('\n', 0, match.start()) - 1
            )
            element_id = f"{file_path}:{name}"
            elements[element_id] = element
        
        return elements, relationships
    
    def _regex_parse_javascript(self, content: str, file_path: str, lines: List[str]) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Regex-based JavaScript parsing."""
        elements = {}
        relationships = []
        
        import re
        
        # Find functions
        func_patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'let\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'var\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
        ]
        
        for pattern in func_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                
                element = CodeElement(
                    name=name,
                    type='function',
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    column_start=match.start() - content.rfind('\n', 0, match.start()) - 1,
                    column_end=match.end() - content.rfind('\n', 0, match.start()) - 1
                )
                element_id = f"{file_path}:{name}"
                elements[element_id] = element
        
        # Find classes
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+\w+)?\s*{'
        for match in re.finditer(class_pattern, content, re.MULTILINE):
            name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type='class',
                file_path=file_path,
                line_start=line_num,
                line_end=line_num,
                column_start=match.start() - content.rfind('\n', 0, match.start()) - 1,
                column_end=match.end() - content.rfind('\n', 0, match.start()) - 1
            )
            element_id = f"{file_path}:{name}"
            elements[element_id] = element
        
        return elements, relationships
    
    def _regex_parse_java(self, content: str, file_path: str, lines: List[str]) -> Tuple[Dict[str, CodeElement], List[Tuple[str, str, str]]]:
        """Regex-based Java parsing."""
        elements = {}
        relationships = []
        
        import re
        
        # Find methods
        method_pattern = r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*{'
        for match in re.finditer(method_pattern, content, re.MULTILINE):
            name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type='function',
                file_path=file_path,
                line_start=line_num,
                line_end=line_num,
                column_start=match.start() - content.rfind('\n', 0, match.start()) - 1,
                column_end=match.end() - content.rfind('\n', 0, match.start()) - 1
            )
            element_id = f"{file_path}:{name}"
            elements[element_id] = element
        
        # Find classes
        class_pattern = r'(?:public\s+)?class\s+(\w+)(?:\s+extends\s+\w+)?(?:\s+implements\s+[^{]+)?\s*{'
        for match in re.finditer(class_pattern, content, re.MULTILINE):
            name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type='class',
                file_path=file_path,
                line_start=line_num,
                line_end=line_num,
                column_start=match.start() - content.rfind('\n', 0, match.start()) - 1,
                column_end=match.end() - content.rfind('\n', 0, match.start()) - 1
            )
            element_id = f"{file_path}:{name}"
            elements[element_id] = element
        
        return elements, relationships
    
    def _get_node_text(self, node: Node, content: str, child_type: str) -> Optional[str]:
        """Extract text from a specific child node type."""
        for child in node.children:
            if child.type == child_type:
                return content[child.start_byte:child.end_byte]
        return None
    
    def _get_import_name(self, node: Node, content: str) -> Optional[str]:
        """Extract import name from import statement."""
        for child in node.children:
            if child.type == 'dotted_name':
                return content[child.start_byte:child.end_byte]
        return None
    
    def _find_function_calls(self, node: Node, content: str, parent_id: str, elements: Dict[str, CodeElement], relationships: List[Tuple[str, str, str]], file_path: str):
        """Find function calls within a node."""
        # This is a simplified implementation
        # In a real implementation, you'd traverse the AST to find call expressions
        pass
    
    def _get_code_files(self, repo_path: Path, language: str) -> List[Path]:
        """Get all code files for the specified language."""
        extensions = {
            'python': ['.py'],
            'jac': ['.jac'],
            'javascript': ['.js', '.jsx'],
            'java': ['.java'],
            'cpp': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
            'rust': ['.rs'],
            'go': ['.go']
        }
        
        lang_extensions = extensions.get(language, [])
        code_files = []
        
        for ext in lang_extensions:
            code_files.extend(repo_path.rglob(f'*{ext}'))
        
        return code_files
    
    def query_relationships(self, ccg: CodeContextGraph, query: str) -> List[Dict[str, Any]]:
        """Query relationships in the Code Context Graph."""
        results = []
        
        # Simple query examples
        if "calls" in query.lower():
            # Find function calls
            for from_id, to_id, rel_type in ccg.relationships:
                if rel_type == 'calls':
                    results.append({
                        'from': from_id,
                        'to': to_id,
                        'relationship': rel_type
                    })
        
        elif "inherits" in query.lower():
            # Find inheritance relationships
            for from_id, to_id, rel_type in ccg.relationships:
                if rel_type == 'inherits':
                    results.append({
                        'from': from_id,
                        'to': to_id,
                        'relationship': rel_type
                    })
        
        return results


def analyze_codebase(repo_path: str, language: str, entry_points: List[str]) -> CodeContextGraph:
    """
    Convenience function to analyze a codebase.
    
    Args:
        repo_path: Path to the repository
        language: Primary programming language
        entry_points: List of entry point files
        
    Returns:
        CodeContextGraph object
    """
    analyzer = CodeAnalyzer()
    return analyzer.analyze_codebase(repo_path, language, entry_points)