# AutoCAD MCP Tools Specification
## Advanced Algorithmic Coding Partner - MCP Interface Definition

> **Version**: 1.0  
> **Date**: August 6, 2025  
> **Status**: Technical Specification  
> **Purpose**: Transform AutoCAD_MCP into an enterprise-grade algorithmic coding partner through 25+ advanced MCP tools

## Executive Summary

This specification defines the MCP (Model Context Protocol) interface for exposing 25,518+ lines of existing sophisticated code through advanced algorithmic tools. The focus is on creating an AI-powered coding partner that generates complex geometric processing algorithms, multi-language automation workflows, and research-grade mathematical implementations in real-time.

**Critical Missing Component**: C# .NET code generation is identified as the highest priority gap preventing enterprise AutoCAD developer adoption.

## Architecture Overview

### Integration Strategy
- **Leverage Existing Code**: All MCP tools expose existing sophisticated implementations rather than creating new ones
- **Natural Language Interface**: Advanced algorithms accessible through conversational AI
- **Multi-Language Synthesis**: Coordinated code generation across Python, C#, AutoLISP, VBA
- **Real-Time Execution**: Complex algorithms generated and executed within seconds
- **Enterprise Security**: Comprehensive audit logging, sandboxing, and access controls

### Core Principles
1. **Advanced Over Basic**: Focus on sophisticated algorithms, not simple drawing commands
2. **Research-Grade Quality**: Mathematical implementations meet academic standards
3. **Production Ready**: Generated code includes comprehensive error handling and optimization
4. **Multi-Domain**: Geometric processing, AI-powered synthesis, enterprise collaboration
5. **Extensible Architecture**: Plugin system for additional algorithm domains

---

## Category 1: Advanced Geometric Processing Tools

### 1.1 unfold_3d_surface
**Exposes**: `/src/algorithms/lscm.py` (334 lines) - LSCM algorithm implementation

**Description**: Advanced 3D surface unfolding using Least Squares Conformal Mapping with minimal distortion for manufacturing applications.

**Parameters**:
```json
{
  "surface_geometry": {
    "type": "object",
    "properties": {
      "vertices": {"type": "array", "items": {"type": "array", "minItems": 3, "maxItems": 3}},
      "triangles": {"type": "array", "items": {"type": "array", "minItems": 3, "maxItems": 3}},
      "normals": {"type": "array", "items": {"type": "array", "minItems": 3, "maxItems": 3}}
    },
    "required": ["vertices", "triangles"]
  },
  "unfolding_method": {
    "type": "string",
    "enum": ["lscm", "angle_based", "harmonic"],
    "default": "lscm"
  },
  "distortion_constraints": {
    "type": "object",
    "properties": {
      "max_angle_distortion": {"type": "number", "minimum": 0, "maximum": 180, "default": 15},
      "max_area_distortion": {"type": "number", "minimum": 0, "maximum": 5.0, "default": 1.2},
      "preserve_boundaries": {"type": "boolean", "default": true}
    }
  },
  "manufacturing_parameters": {
    "type": "object",
    "properties": {
      "material_thickness": {"type": "number", "minimum": 0},
      "bend_radius": {"type": "number", "minimum": 0},
      "cutting_tolerance": {"type": "number", "minimum": 0, "default": 0.1}
    }
  }
}
```

**Returns**:
```json
{
  "unfolded_pattern": {
    "vertices_2d": [["number", "number"]],
    "edges": [["integer", "integer"]],
    "cutting_paths": [["number", "number"]]
  },
  "distortion_analysis": {
    "angle_distortion_map": [["number"]],
    "area_distortion_map": [["number"]],
    "max_distortion": {"angle": "number", "area": "number"},
    "quality_score": {"type": "number", "minimum": 0, "maximum": 1}
  },
  "manufacturing_data": {
    "cutting_instructions": {"type": "string"},
    "bend_lines": [["number", "number", "number", "number"]],
    "material_utilization": {"type": "number"},
    "estimated_waste": {"type": "number"}
  }
}
```

**Usage Examples**:
```
User: "Unfold this cylindrical surface for sheet metal fabrication with minimal distortion"
→ Generates complete LSCM unfolding with manufacturing constraints

User: "I need to create a developable surface pattern for a complex architectural facade"
→ Returns optimized 2D pattern with distortion analysis and cutting instructions
```

**Performance**: Sub-10 second execution for meshes up to 50,000 triangles

---

### 1.2 calculate_geodesics
**Exposes**: `/src/algorithms/geodesic.py` (361 lines) - Advanced geodesic calculations

**Description**: Compute geodesic distances and optimal paths on 3D surfaces for structural analysis and path optimization.

**Parameters**:
```json
{
  "surface_geometry": {
    "type": "object",
    "properties": {
      "vertices": {"type": "array"},
      "triangles": {"type": "array"},
      "edge_weights": {"type": "array", "description": "Optional custom edge weights"}
    }
  },
  "calculation_type": {
    "type": "string",
    "enum": ["single_source", "all_pairs", "path_optimization", "heat_method"],
    "default": "single_source"
  },
  "source_points": {"type": "array", "items": {"type": "integer"}},
  "target_points": {"type": "array", "items": {"type": "integer"}},
  "constraints": {
    "type": "object",
    "properties": {
      "avoid_regions": {"type": "array"},
      "preferred_regions": {"type": "array"},
      "maximum_curvature": {"type": "number"}
    }
  }
}
```

**Returns**:
```json
{
  "geodesic_distances": {"type": "array"},
  "optimal_paths": [{"path": ["integer"], "distance": "number", "curvature": "number"}],
  "distance_field": {"type": "array", "description": "Heat-based distance field"},
  "analysis": {
    "path_efficiency": "number",
    "curvature_analysis": {"max": "number", "mean": "number", "variance": "number"},
    "computational_time": "number"
  }
}
```

---

### 1.3 optimize_material_patterns
**Exposes**: `/src/pattern_optimization.py` - Genetic algorithm optimization

**Description**: Advanced material nesting optimization using genetic algorithms for laser cutting and manufacturing.

**Parameters**:
```json
{
  "shapes_data": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "geometry": {"type": "array", "description": "Polygon vertices"},
        "quantity": {"type": "integer", "minimum": 1},
        "rotation_allowed": {"type": "boolean", "default": true},
        "priority": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5}
      }
    }
  },
  "material_constraints": {
    "type": "object",
    "properties": {
      "sheet_dimensions": {"type": "array", "minItems": 2, "maxItems": 2},
      "material_cost_per_unit": {"type": "number"},
      "cutting_kerf": {"type": "number", "default": 0.1},
      "minimum_spacing": {"type": "number", "default": 1.0}
    }
  },
  "optimization_parameters": {
    "type": "object",
    "properties": {
      "algorithm": {"type": "string", "enum": ["genetic", "simulated_annealing", "bottom_left_fill"], "default": "genetic"},
      "population_size": {"type": "integer", "minimum": 10, "maximum": 500, "default": 100},
      "generations": {"type": "integer", "minimum": 1, "maximum": 1000, "default": 200},
      "mutation_rate": {"type": "number", "minimum": 0, "maximum": 1, "default": 0.1}
    }
  }
}
```

**Returns**:
```json
{
  "optimized_layout": {
    "placed_shapes": [{"shape_id": "integer", "position": ["number", "number"], "rotation": "number"}],
    "material_utilization": {"type": "number"},
    "waste_percentage": {"type": "number"}
  },
  "cutting_instructions": {
    "cutting_paths": [["number", "number"]],
    "path_optimization": {"total_distance": "number", "estimated_time": "number"},
    "tool_changes": ["string"]
  },
  "cost_analysis": {
    "material_cost": "number",
    "cutting_time": "number",
    "waste_cost": "number",
    "total_cost": "number"
  }
}
```

---

### 1.4 process_complex_meshes
**Exposes**: `/src/algorithms/mesh_utils.py` (370 lines) - Advanced mesh processing

**Description**: Comprehensive mesh processing including smoothing, repair, simplification, and quality analysis.

**Parameters**:
```json
{
  "mesh_data": {
    "type": "object",
    "properties": {
      "vertices": {"type": "array"},
      "faces": {"type": "array"},
      "normals": {"type": "array", "description": "Optional vertex normals"}
    }
  },
  "operations": {
    "type": "array",
    "items": {
      "type": "string",
      "enum": ["smooth", "repair", "simplify", "remesh", "analyze_quality", "detect_features"]
    }
  },
  "parameters": {
    "type": "object",
    "properties": {
      "smoothing_iterations": {"type": "integer", "default": 5},
      "simplification_ratio": {"type": "number", "minimum": 0, "maximum": 1, "default": 0.1},
      "feature_angle": {"type": "number", "default": 30},
      "repair_holes": {"type": "boolean", "default": true}
    }
  }
}
```

---

### 1.5 generate_cutting_patterns
**New Implementation** - Integrates with existing optimization algorithms

**Description**: Generate optimized cutting patterns for complex 3D geometries with manufacturing constraints.

---

## Category 2: AI-Powered Code Generation Tools

### 2.1 generate_algorithm_from_description
**Exposes**: `/src/ai_features/ai_code_generator.py` (1,250 lines) - Sophisticated AI code generation

**Description**: Transform natural language descriptions into working geometric processing algorithms with full implementation.

**Parameters**:
```json
{
  "problem_description": {
    "type": "string",
    "description": "Natural language description of the algorithmic problem"
  },
  "target_language": {
    "type": "string",
    "enum": ["python", "csharp", "autolisp", "vba"],
    "default": "python"
  },
  "complexity_level": {
    "type": "string",
    "enum": ["prototype", "production", "research_grade"],
    "default": "production"
  },
  "performance_requirements": {
    "type": "object",
    "properties": {
      "max_execution_time": {"type": "number", "description": "Seconds"},
      "memory_limit": {"type": "number", "description": "MB"},
      "accuracy_threshold": {"type": "number", "minimum": 0, "maximum": 1}
    }
  },
  "integration_context": {
    "type": "object",
    "properties": {
      "autocad_version": {"type": "string"},
      "required_libraries": {"type": "array", "items": {"type": "string"}},
      "existing_codebase_context": {"type": "string"}
    }
  }
}
```

**Returns**:
```json
{
  "generated_code": {
    "main_implementation": "string",
    "supporting_functions": ["string"],
    "test_cases": ["string"],
    "documentation": "string"
  },
  "algorithm_analysis": {
    "complexity_analysis": {"time": "string", "space": "string"},
    "mathematical_basis": "string",
    "limitations": ["string"],
    "optimization_opportunities": ["string"]
  },
  "integration_instructions": {
    "setup_steps": ["string"],
    "dependencies": ["string"],
    "usage_examples": ["string"],
    "troubleshooting": ["string"]
  }
}
```

**Usage Examples**:
```
User: "I need an algorithm to detect and classify geometric features in 3D CAD models for manufacturing analysis"
→ Generates complete feature recognition system with shape analysis

User: "Create a structural optimization algorithm that minimizes weight while maintaining stiffness constraints"
→ Returns topology optimization implementation with FEA integration
```

---

### 2.2 translate_natural_language_to_code
**Exposes**: `/src/ai_features/natural_language_processor.py` (886 lines) - NLP to code translation

**Description**: Advanced natural language processing that converts technical descriptions into executable code.

**Parameters**:
```json
{
  "natural_language_input": {"type": "string"},
  "domain_context": {
    "type": "string",
    "enum": ["geometric_processing", "structural_analysis", "manufacturing", "automation", "data_analysis"]
  },
  "output_preferences": {
    "type": "object",
    "properties": {
      "code_style": {"type": "string", "enum": ["verbose", "concise", "educational"]},
      "include_comments": {"type": "boolean", "default": true},
      "include_error_handling": {"type": "boolean", "default": true}
    }
  }
}
```

---

### 2.3 synthesize_automation_workflow
**Leverages**: Multiple existing systems for comprehensive workflow creation

**Description**: Create complex multi-step automation workflows that coordinate multiple algorithms and processes.

**Parameters**:
```json
{
  "workflow_description": {"type": "string"},
  "input_data_types": {"type": "array", "items": {"type": "string"}},
  "output_requirements": {"type": "array", "items": {"type": "string"}},
  "error_handling_strategy": {
    "type": "string",
    "enum": ["strict", "graceful", "custom"],
    "default": "graceful"
  },
  "performance_requirements": {
    "type": "object",
    "properties": {
      "parallel_execution": {"type": "boolean", "default": false},
      "memory_optimization": {"type": "boolean", "default": true},
      "progress_tracking": {"type": "boolean", "default": true}
    }
  }
}
```

---

### 2.4 generate_csharp_autocad_code ⭐ **CRITICAL MISSING COMPONENT**
**Status**: **NEW IMPLEMENTATION REQUIRED** - Highest Priority

**Description**: Generate production-ready C# code for AutoCAD .NET API, ObjectARX integration, and advanced AutoCAD development.

**Rationale**: C# is the primary language for professional AutoCAD development. This gap prevents adoption by enterprise developers who need:
- ObjectARX plugin development
- Advanced .NET API utilization
- Performance-critical AutoCAD applications
- Enterprise-grade error handling and logging

**Parameters**:
```json
{
  "code_requirements": {
    "type": "object",
    "properties": {
      "target_framework": {"type": "string", "enum": [".NET Framework 4.8", ".NET 6", ".NET 8"], "default": ".NET Framework 4.8"},
      "autocad_api_level": {"type": "string", "enum": ["managed_net", "objectarx", "hybrid"]},
      "functionality_type": {"type": "string", "enum": ["command", "plugin", "application", "library"]}
    }
  },
  "algorithm_specification": {"type": "string"},
  "performance_requirements": {
    "type": "object",
    "properties": {
      "real_time_constraints": {"type": "boolean"},
      "memory_efficiency": {"type": "string", "enum": ["standard", "optimized", "enterprise"]},
      "thread_safety": {"type": "boolean", "default": true}
    }
  },
  "integration_requirements": {
    "type": "object",
    "properties": {
      "database_access": {"type": "boolean"},
      "ui_components": {"type": "boolean"},
      "external_libraries": {"type": "array", "items": {"type": "string"}},
      "licensing_model": {"type": "string", "enum": ["single_user", "network", "subscription"]}
    }
  }
}
```

**Returns**:
```json
{
  "csharp_implementation": {
    "main_class": "string",
    "command_classes": ["string"],
    "utility_classes": ["string"],
    "configuration_files": ["string"]
  },
  "project_structure": {
    "solution_file": "string",
    "project_file": "string",
    "assembly_info": "string",
    "references": ["string"]
  },
  "deployment_package": {
    "installer_script": "string",
    "registration_commands": ["string"],
    "documentation": "string",
    "example_usage": ["string"]
  }
}
```

**Implementation Requirements**:
- **Template System**: Comprehensive C# templates for AutoCAD development patterns
- **API Integration**: Deep integration with AutoCAD .NET API documentation and best practices
- **Error Handling**: Enterprise-grade exception handling and logging
- **Performance Optimization**: Memory management and performance profiling
- **Testing Framework**: Automated testing for AutoCAD plugins
- **Documentation Generation**: Comprehensive API documentation

---

### 2.5 create_multi_language_solution
**Exposes**: `/src/code_generation/language_coordinator.py` - Multi-language coordination

**Description**: Create comprehensive solutions that coordinate Python, C#, AutoLISP, and VBA components for complex automation workflows.

---

## Category 3: Interactive Development Tools

### 3.1 advanced_code_debugging
**Exposes**: `/src/interactive/debugger.py` and related interactive tools

**Description**: Advanced debugging capabilities with breakpoint management, variable inspection, and performance profiling.

**Parameters**:
```json
{
  "code_to_debug": {"type": "string"},
  "language": {"type": "string", "enum": ["python", "csharp", "autolisp", "vba"]},
  "debug_configuration": {
    "type": "object",
    "properties": {
      "breakpoint_strategy": {"type": "string", "enum": ["conditional", "exception", "performance"]},
      "variable_tracking": {"type": "boolean", "default": true},
      "performance_profiling": {"type": "boolean", "default": false}
    }
  }
}
```

---

### 3.2 intelligent_code_refactoring
**Exposes**: `/src/interactive/code_refactoring.py` (997 lines) - AST-based refactoring

**Description**: Advanced code refactoring using Abstract Syntax Tree analysis and AutoCAD-specific optimization patterns.

---

### 3.3 performance_analysis_and_optimization
**Exposes**: `/src/interactive/performance_analyzer.py` (788 lines) - Performance analysis

**Description**: Comprehensive performance analysis with optimization recommendations for AutoCAD algorithms.

---

### 3.4 variable_inspection_and_profiling
**Exposes**: `/src/interactive/variable_inspector.py` (986 lines) - Advanced variable inspection

**Description**: Deep variable inspection with AutoCAD object specialization and memory tracking.

---

### 3.5 secure_code_execution
**Exposes**: `/src/interactive/security_sandbox.py` - Secure execution environment

**Description**: Sandboxed code execution with comprehensive security monitoring for enterprise environments.

---

## Category 4: Enterprise Integration Tools

### 4.1 collaboration_real_time_editing
**Exposes**: `/src/enterprise/collaboration_architecture.py` - Multi-user collaboration

**Description**: Real-time collaborative editing with operational transformation for distributed development teams.

---

### 4.2 security_audit_and_monitoring
**Exposes**: `/src/enterprise/security_monitoring.py` - Security monitoring system

**Description**: Comprehensive security monitoring with audit trails, threat detection, and compliance reporting.

---

### 4.3 deployment_automation_pipeline
**Exposes**: `/src/enterprise/deployment_automation.py` - Deployment automation

**Description**: Automated deployment with Docker/Kubernetes support and multi-environment pipeline management.

---

### 4.4 performance_monitoring_dashboard
**Exposes**: `/src/enterprise/monitoring_dashboard.py` - Performance monitoring

**Description**: Advanced analytics dashboard with anomaly detection and predictive forecasting.

---

### 4.5 enterprise_analytics_reporting
**Exposes**: Integration of multiple enterprise monitoring systems

**Description**: Comprehensive analytics and reporting for enterprise AutoCAD development environments.

---

## Category 5: Multi-Language Code Synthesis Tools

### 5.1 generate_vba_macro
**Exposes**: `/src/code_generation/vba_generator.py` (1,048 lines) - VBA generation

**Description**: Generate sophisticated VBA macros with mathematical libraries and advanced AutoCAD integration.

---

### 5.2 create_python_scientific_script
**Exposes**: `/src/code_generation/python_generator.py` (1,020 lines) - Python generation

**Description**: Generate Python scripts with NumPy, SciPy integration for scientific computing applications.

---

### 5.3 synthesize_autolisp_routine
**Exposes**: `/src/code_generation/autolisp_generator.py` (699 lines) - AutoLISP generation

**Description**: Create advanced AutoLISP routines for geometric processing and AutoCAD automation.

---

### 5.4 compile_csharp_dotnet_solution ⭐ **CRITICAL NEW IMPLEMENTATION**
**Status**: **REQUIRES NEW DEVELOPMENT** - Critical for enterprise adoption

**Description**: Complete C# .NET solution compilation with ObjectARX integration, professional deployment, and enterprise features.

**Integration with 2.4**: This tool provides the compilation and deployment capabilities for the C# code generated by `generate_csharp_autocad_code`.

---

### 5.5 coordinate_multi_language_workflow
**Exposes**: `/src/code_generation/language_coordinator.py` - Multi-language coordination

**Description**: Orchestrate complex workflows that span multiple programming languages with data exchange and synchronization.

---

## Implementation Priorities

### Phase 1: Immediate High-Value Integration (Weeks 1-2)
1. **unfold_3d_surface** - Expose existing LSCM algorithm
2. **generate_algorithm_from_description** - Expose AI code generator
3. **process_complex_meshes** - Expose mesh processing utilities
4. **intelligent_code_refactoring** - Expose refactoring engine

### Phase 2: Critical Missing Components (Weeks 3-4)
1. **generate_csharp_autocad_code** - **CRITICAL NEW DEVELOPMENT**
2. **compile_csharp_dotnet_solution** - **CRITICAL NEW DEVELOPMENT**
3. **optimize_material_patterns** - Expose genetic optimization
4. **translate_natural_language_to_code** - Expose NLP processor

### Phase 3: Enterprise Integration (Weeks 5-6)
1. **collaboration_real_time_editing** - Expose collaboration architecture
2. **security_audit_and_monitoring** - Expose security monitoring
3. **performance_monitoring_dashboard** - Expose monitoring dashboard
4. **synthesize_automation_workflow** - Create workflow coordinator

### Phase 4: Advanced Algorithmic Tools (Weeks 7-8)
1. **calculate_geodesics** - Expose geodesic calculations
2. **generate_cutting_patterns** - New cutting pattern generator
3. **create_multi_language_solution** - Advanced multi-language coordination
4. **enterprise_analytics_reporting** - Comprehensive analytics

## Security and Authentication Framework

### Authentication Requirements
- **API Keys**: Secure API key management with role-based access
- **Session Management**: Secure session handling with timeout controls
- **Audit Logging**: Comprehensive logging of all tool usage and code generation
- **Sandboxing**: Secure execution environment for generated code

### Enterprise Security Features
- **Code Signing**: Digital signatures for generated code packages
- **Threat Detection**: Real-time monitoring for malicious code patterns
- **Compliance Reporting**: SOX, GDPR, and industry-specific compliance
- **Access Controls**: Fine-grained permissions for different tool categories

## Performance and Scalability Requirements

### Performance Targets
- **Algorithm Generation**: Sub-5 second response for standard complexity
- **Complex Algorithms**: Sub-30 second response for research-grade implementations
- **Concurrent Users**: Support 100+ concurrent users per server instance
- **Memory Efficiency**: Maximum 2GB RAM per active session

### Scalability Architecture
- **Horizontal Scaling**: Container-based scaling with load balancing
- **Caching Layer**: Intelligent caching of frequently used algorithms
- **Resource Pooling**: Shared computational resources for optimization algorithms
- **Auto-scaling**: Dynamic scaling based on demand patterns

## Error Handling and Edge Cases

### Comprehensive Error Management
- **Input Validation**: Strict validation of all input parameters
- **Graceful Degradation**: Fallback mechanisms for failed operations
- **Error Recovery**: Automatic retry mechanisms with exponential backoff
- **User-Friendly Messages**: Clear error messages with suggested solutions

### Edge Case Handling
- **Large Dataset Processing**: Streaming processing for large meshes and datasets
- **Memory Limitations**: Automatic optimization for memory-constrained environments
- **Network Failures**: Robust handling of network interruptions
- **Algorithm Convergence**: Detection and handling of non-convergent algorithms

## Integration Architecture

### MCP Protocol Integration
```json
{
  "protocol_version": "2024-11-05",
  "server_info": {
    "name": "AutoCAD Advanced Algorithmic Partner",
    "version": "1.0.0"
  },
  "capabilities": {
    "tools": 25,
    "resources": ["algorithm_library", "template_repository", "performance_metrics"],
    "prompts": ["algorithm_explanation", "optimization_suggestions", "integration_guidance"]
  }
}
```

### External System Integration
- **AutoCAD COM Integration**: Direct integration with AutoCAD through COM interface
- **File System Access**: Secure access to AutoCAD drawings and project files
- **Database Connectivity**: Integration with enterprise databases and PLM systems
- **Cloud Services**: Integration with cloud-based CAD and analysis platforms

## Success Metrics and Validation

### Performance Metrics
- **Algorithm Accuracy**: Validation against known mathematical benchmarks
- **Code Quality**: Automated code quality scoring and best practice compliance
- **User Satisfaction**: User feedback scores and adoption metrics
- **System Reliability**: Uptime, error rates, and performance consistency

### Validation Framework
- **Mathematical Validation**: Automated testing against published algorithm results
- **Code Testing**: Comprehensive unit and integration testing for all generated code
- **Performance Benchmarking**: Regular performance comparison against industry standards
- **User Acceptance Testing**: Structured testing with target user groups

---

## Conclusion

This specification defines a comprehensive transformation of AutoCAD_MCP from a basic drawing assistant into an advanced algorithmic coding partner. The focus on exposing existing sophisticated code through intelligent MCP interfaces, combined with the critical addition of C# .NET capabilities, positions this system as a revolutionary tool for professional AutoCAD development.

**Key Success Factors**:
1. **Leverage Existing Assets**: 25,518+ lines of sophisticated code become immediately accessible
2. **Fill Critical Gaps**: C# .NET integration enables enterprise adoption
3. **Natural Language Interface**: Complex algorithms become accessible to broader audience
4. **Enterprise Grade**: Security, performance, and scalability meet enterprise requirements
5. **Multi-Domain Expertise**: Geometric processing, AI synthesis, and workflow automation

**Expected Impact**: Transform AutoCAD automation from manual coding to AI-powered algorithmic synthesis, reducing complex algorithm development from weeks to minutes while maintaining research-grade quality and enterprise reliability.