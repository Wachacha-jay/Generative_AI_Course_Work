import os;
import json;
import time;
import from jac_utils { map_repository, analyze_codebase, generate_documentation, save_documentation };

# Node definitions
node Repository {
    has url;
    has name;
    has local_path;
    has repo_info;
    has language_detection;
    has entry_points;
    has message;
    has file_tree;
    
    can init {
        # Initialize with default values
        url = "";
        name = "";
        local_path = "";
        repo_info = {};
        language_detection = {};
        entry_points = [];
        message = "";
        file_tree = {};
    }
}


walker repo_mapper: api {
    has repo_map = {};
    has url = "";
    has response = {};
    
    can start {
        if(!url): url = "https://github.com/Wachacha-jay/Recommender_system";
        print("Starting repository mapping...");
        visit [-->];
    }

    can map_repo with Repository {
        print("Mapping repository at: " + url);
        response = map_repository(url);
        if(response["success"]) {
            here.url = url;
            here.name = response["repo_name"];
            here.local_path = response["local_path"];
            here.repo_info = response["repo_info"];
            here.language_detection = response["language_detection"];
            here.entry_points = response["entry_points"];
            here.message = response["message"];
            here.file_tree = response["file_tree"];
            report response;
        } else {
            report {"success": false, "error": response["error"]};
        }
    }

    can get_repo_info: api_exposed {
        return {
            "url": here.url,
            "name": here.name,
            "local_path": here.local_path,
            "language_detection": here.language_detection,
            "entry_points": here.entry_points,
            "file_tree": here.file_tree
        };
    }
}

walker code_analyzer: api {
    has analysis_result = {};
    has response = {};

    can start {
        print("Starting code analysis...");
        visit [-->];
    }

    can analyze with Repository {
        print("Starting code analysis for repository: " + here.url);
        response = analyze_codebase(
            here.local_path,
            here.language_detection["primary_language"],
            here.entry_points
        );

        if(response["success"]) {
            analysis_result = response;
            report response;
        } else {
            report {"success": false, "error": response["error"]};
        }
    }

    can get_analysis: api_exposed {
        return analysis_result;
    }
}

walker doc_generator: api {
    has documentation = {};
    has response = {};
    has ccg = {};

    can start {
        print("Starting documentation generation...");
        visit [-->];
    }

    can generate_docs with Repository {
        print("Generating documentation for repository: " + here.url);
        response = generate_documentation(
            {
                "repo_info": here.repo_info,
                "language_detection": here.language_detection,
                "entry_points": here.entry_points,
                "file_tree": here.file_tree
            },
            ccg,
            here.name
        );

        if(response["success"]) {
            documentation = response["documentation"];
            report response;
        } else {
            report {"success": false, "error": response["error"]};
        }
    }

    can get_documentation: api_exposed {
        return documentation;
    }
}

walker doc_saver: api {
    has response = {};

    can start {
        print("Starting documentation saving...");
        visit [-->];
    }

    can save_docs with Repository {
        print("Saving documentation for repository: " + here.url);
        try {
            doc_path = save_documentation(here.documentation, here.name);
            report {
                "success": true,
                "message": "Documentation saved successfully",
                "path": doc_path
            };
        } else {
            report {
                "success": false,
                "error": "Failed to save documentation"
            };
        }
    }
}

with entry {
    print("Agentic Codebase Genius API Server started.");
    print("==========================================");
    
    # Create root repository node
    root = spawn here --> node::Repository;
    
    # Start serving API endpoints
    spawn {
        "name": "repo_mapper",
        "preset": "public",
        "port": 8000
    } --> walker::repo_mapper;
    
    spawn {
        "name": "code_analyzer",
        "preset": "public",
        "port": 8001
    } --> walker::code_analyzer;
    
    spawn {
        "name": "doc_generator",
        "preset": "public",
        "port": 8002
    } --> walker::doc_generator;
    
    spawn {
        "name": "doc_saver",
        "preset": "public",
        "port": 8003
    } --> walker::doc_saver;
    
    print("All API endpoints are now active.");
}