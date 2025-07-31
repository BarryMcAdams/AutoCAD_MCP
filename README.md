<div align="center">

# 🚀 AutoCAD MCP Server

<p align="center">
  <strong>The AI-powered copilot for modern Computer-Aided Design.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/AutoCAD-2021--2025-orange.svg" alt="AutoCAD Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg" alt="Status">
</p>

---

</div>

## ✨ Overview

This **AutoCAD MCP Server** is a comprehensive Model Context Protocol (MCP) server designed to assist my AutoCAD development and manufacturing workflows. This advanced system integrates cutting-edge AI capabilities with AutoCAD 2025, providing developers and engineers with powerful tools for automation, code generation, and intelligent design assistance. 

Built with **Python 3.12** and leveraging **Flask 3.0**, this mcp server was made to turn some of my traditional CAD processes into intelligent, automated workflows that enhance productivity and innovation across the manufacturing and design industries.

### 🎯 Target Audience

**TARGET AUDIENCE:** CAD and code programming professionals involved in engineering, manufacturing, and architecture using AutoCAD 2025 on Windows, who may want to author custom utilities for 3D-to-2D transformations and presentation automation.

---

## 🌟 Key Features

| Feature | Description |
| :--- | :--- |
| 🤖 **AI-Powered Development** | Use natural language to generate Python and AutoLISP scripts, get API recommendations, and even predict errors before they happen. |
| 🏭 **Advanced Manufacturing** | Automate complex tasks like 3D surface unfolding, parametric design, and pattern optimization for maximum material efficiency. |
| 🏢 **Enterprise Ready** | Built for professional teams with features like multi-user collaboration, security monitoring, and deployment automation. |
| 🛠️ **Developer Tools** | A comprehensive development framework with a mock AutoCAD system for offline testing, performance benchmarking, and CI/CD integration. |

## 🚀 Getting Started

We have two main guides to help you get started, depending on your background:

### For AutoCAD Drafters (No Coding Experience)

If you're an AutoCAD user who wants to use AI to automate your work, we have a set of detailed, non-technical guides for you. Start here:

➡️ **[The AutoCAD Drafter's Guide to Installation & Setup](./docs/01-Installation-Setup.md)**

### For Developers

If you're a developer who wants to build on top of the AutoCAD MCP Server, you can get started with the following steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BarryMcAdams/AutoCAD_MCP.git
    cd AutoCAD_MCP
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server:**
    ```bash
    python src/mcp_server.py
    ```

For more detailed information, please refer to the [developer documentation](./docs/README.md).

## 🏗️ Architecture Overview

The AutoCAD MCP Server is built on a modular and scalable architecture. It uses a powerful Python wrapper to communicate with the AutoCAD COM API, and a flexible MCP server framework to expose the AI-powered tools. This design allows for easy extension and integration with other systems.

<div align="center">

```mermaid
graph TD
    A[AutoCAD User / Developer] --> B{Claude Desktop / MCP Client};
    B --> C{AutoCAD MCP Server (Python)};
    C --> D[Enhanced AutoCAD Wrapper];
    D --> E[AutoCAD Application];
```

</div>

## 💼 Use Cases

*   **Manufacturing:** Automate the creation of flat patterns for sheet metal, HVAC, and other fabrication industries.
*   **Architecture:** Generate complex and parametric designs for buildings, facades, and other architectural elements.
*   **Product Design:** Quickly create and iterate on 3D models of products, parts, and assemblies.
*   **Automation:** Build custom tools and workflows to automate your company's specific AutoCAD processes.

## 🤝 Contributing

We welcome contributions from the community! Whether you're a developer, a CAD expert, or just an enthusiastic user, there are many ways to get involved:

*   **Report bugs:** If you find a bug, please open an issue on our [GitHub Issues](https://github.com/BarryMcAdams/AutoCAD_MCP/issues) page.
*   **Suggest features:** Have a great idea for a new feature? Let us know on our [GitHub Discussions](https://github.com/BarryMcAdams/AutoCAD_MCP/discussions) page.
*   **Contribute code:** If you're a developer, we welcome pull requests! Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) file for more information.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

This project would not be possible without the following:

*   [Python](https://www.python.org/)
*   [AutoCAD](https://www.autodesk.com/products/autocad/overview)
*   [Flask](https://flask.palletsprojects.com/)
*   [pyautocad](https://pypi.org/project/pyautocad/)
*   And the many other open-source libraries.

Special thanks to the AutoCAD community for their support and feedback.

---

<div align="center">
## 🎯 **AutoCAD MCP Server** - Transforming Manufacturing CAD Workflows

**With love ❤️ to our amazing AutoCAD community around the world ~ [Barry Adams](mailto:info@CADcoLabs.com), Florida USA**

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red.svg" alt="Made with Love">
  <img src="https://img.shields.io/badge/For-AutoCAD%20Community-blue.svg" alt="For AutoCAD Community">
  <img src="https://img.shields.io/badge/Ready-Production-brightgreen.svg" alt="Production Ready">
</p>
</div>
