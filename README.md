<a name="start-building"></a>

<p align="center">
<img src="img/banner-ai-tour-27.png" alt="Microsoft AI Tour 2027" width="100%"/>
</p>

# [Microsoft AI Tour 2027](https://aitour.microsoft.com)

## 🔥 ILL335: Building & Deploying AI Agents with Microsoft Foundry

### Session description

Step into the role of an AI developer on Caldova's commercial digital and customer engagement team and build a B2C consumer sentiment analysis tool for Caldova, Microsoft's fictional global pharmaceutical company. You'll discover and provision hosted models in Microsoft Foundry, send your first inference with the Azure AI Projects SDK, build a production-quality sentiment analysis pipeline, and deploy it as a hosted agent — all without fine-tuning or managing infrastructure.

### 🚀 Getting started

#### In a guided session

If you're following along during a live session:

1. Clone this repository and open it in VS Code
2. Complete [Setup](setup/SETUP.md) to provision Azure resources and configure your environment
3. Work through the lab modules in [`docs/`](docs/README.md), starting with [Lab 1: Discover Models](docs/lab1-discover-models.md)

#### On your own

If you're learning at your own pace:

1. Clone this repository
2. Follow [Setup](setup/SETUP.md) to provision Azure infrastructure with `azd` and configure your `.env`
3. Work through the lab modules in [`docs/`](docs/README.md) — Lab 5 (model comparison) is a self-paced extension you can complete at home

### 🎯 Learning outcomes

By the end of this session, you will be able to:

- Discover, provision, and connect to hosted models in Microsoft Foundry using the Azure AI Projects SDK and OpenAI-compatible client — going from zero to a working inference call in minutes
- Build a production-quality consumer sentiment analysis pipeline that classifies feedback and independently routes regulated signals for human review using structured prompts and business logic
- Deploy application logic as a hosted agent on Foundry Agent Service using the Microsoft Agent Framework, the `microsoft.foundry` provider, and `azd up`

### 💻 Technologies used

- Microsoft Foundry (hosted models, projects, and Agent Service)
- Azure AI Projects SDK and the OpenAI Responses API
- Microsoft Agent Framework
- Azure Developer CLI (`azd`) and Bicep for Infrastructure-as-Code
- Python 3.13

### 📚 Continue your learning

Pick your next step based on your learning style:

| Resource | What you'll get |
|----------|-----------------|
| **[Microsoft Ignite ILL335 Presentation](./delivery-resources/ILL335-Attendee-Walkthrough-FY27.pptx)** | Lab Presentation |
| **[Microsoft Learn](https://learn.microsoft.com)** | Official documentation and guided learning paths on these topics |
| **[AI Tour 2027 Resource Center](https://aka.ms/aitour27-resource-center)** | Additional session repos and materials from AI Tour 2027 |
| **[Microsoft Foundry Community](https://aka.ms/MicrosoftFoundryDiscord-AITour27)** | Connect with other learners and experts in our Discord community |

### 🌟 Microsoft Learn MCP Server

The Microsoft Learn MCP Server gives your AI agent direct access to Microsoft's official documentation — grounded, up-to-date answers about the topics in this session.

**GitHub Copilot CLI** — Install with:

```shell
copilot plugin install microsoftdocs/mcp
```

**VS Code** — One-click install:  
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Learn_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft-learn&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D)

For more information, visit the [Learn MCP Server repo](https://aka.ms/learnmcp).

### 👥 Content owners

<table>
<tr>
    <td align="center"><a href="http://github.com/leestott">
        <img src="https://github.com/leestott.png" width="100px;" alt="Lee Stott"/><br />
        <sub><b>Lee Stott</b></sub></a><br />
            <a href="https://github.com/leestott" title="talk">📢</a>
    </td>
    <td align="center"><a href="https://github.com/carlotta94c">
        <img src="https://github.com/carlotta94c.png" width="100px;" alt="Carlotta Castelluccio"/><br />
        <sub><b>Carlotta Castelluccio</b></sub></a><br />
            <a href="https://github.com/carlotta94c" title="talk">📢</a>
    </td>
</tr></table>

### Deliver this session

Presenters and re-delivery partners can find the deck, recordings, presenter
notes, and delivery guidance in [`delivery-resources/`](delivery-resources/README.md).

### ⚖️ Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.

Any use of third-party trademarks or logos are subject to those third-party's policies.
