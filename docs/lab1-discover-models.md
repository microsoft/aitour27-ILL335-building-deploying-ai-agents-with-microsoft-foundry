# Lab 1: Discover Foundry-hosted models

> **Duration:** ~10 minutes

## Scenario

You are an AI developer on Caldova's commercial digital and customer engagement team.Caldova's B2C channels receive thousands of pieces of consumer feedback daily about its products and support services. Your task is to build a **consumer sentiment analysis tool** that classifies feedback sentiment and independently routes regulated signals -- such as potential adverse events, product quality complaints, and medical inquiries -- to the right human reviewers.

In this lab, you will explore the Microsoft Foundry model catalog -- directly inside Visual Studio Code using the **Foundry Toolkit** extension -- to find a model that can power Caldova's consumer sentiment analysis pipeline.

## Objective
Explore the Foundry Toolkit model catalog in Visual Studio Code to discover available hosted models, understand model capabilities, and identify a model suitable for inference-based tasks like product review moderation.

## Step 1: Open the project in VS Code

1. Open Visual Studio Code by launching it from the Start menu or desktop.
2. In VS Code, select **File → Open Folder**.
3. Navigate to the `Desktop` folder, select `AI-Tour-ILL335-main`, and click **Select folder**.
4. When prompted with "Do you trust the authors of the files in this folder?", select **Yes, I trust the authors**.

    ![trust.png](../images/trust.png)
5. You should see the project files in the sidebar.

## Step 2: Open the Foundry Toolkit in Visual Studio Code

The [**Foundry Toolkit** extension](https://aka.ms/ftk_install) is already installed on the lab virtual machine, so you can explore models without leaving your editor -- no web browser required.

1. In the **Activity Bar** on the left, click the **Foundry Toolkit** icon to open the toolkit panel.

    ![Foundry Toolkit Icon](../images/ftk_icon.png)
2. Click **Set Foundry Project → Switch Project → Sign in to Azure**.
3. When prompted to sign in to Azure to access your Foundry resources, use the following Azure credentials:

    Username: +++@lab.CloudPortalCredential(User1).Username+++

    If prompted for a Temporary Access Pass (TAP): +++@lab.CloudPortalCredential(User1).AccessToken+++

    If prompted for a Password: +++@lab.CloudPortalCredential(User1).Password+++
4. After signing in, select the Foundry project that shows up in the list. This is the project pre-provisioned for you in the lab environment, and it contains the model deployments you will use for Caldova's consumer sentiment analysis system.

The toolkit panel is your central hub for browsing models, testing them in a playground, and working with agents -- all from within VS Code.

## Step 3: Explore the model catalog

1. In the Foundry Toolkit panel, under **Developer Tools**, select **Model Catalog** to open the model catalog view. These are production-ready, hosted models you can use without fine-tuning.

    ![Model Catalog](../images/model_catalog.png)
2. Browse the available models. Use the filters at the top of the catalog to narrow the list -- for example, by Publisher (Azure OpenAI, Microsoft, Meta, Mistral, etc.), by where the model is **hosted by** (such as Microsoft Foundry), or by task (Responses, Image Analysis, etc.).

Select a model to view its model card. Take note of the following properties.

| Property | Common values |
|----------|---------------|
| Model provider | Azure OpenAI, Microsoft AI, Meta, Mistral, etc. |
| Task type | Responses, embeddings, text to image |
| Input type | text, image |
| Output type | text, image |
| Context window | Varies by model (see model card) |
| Token limits | Varies by model (see model card) |

## Step 4: Identify a model for this lab

For this workshop, you need a model that supports the **Responses API** -- the ability to accept instructions and input and return structured response text.

Recommended models for this lab:

| Model | Publisher | Why |
|-------|-----------|-----|
| gpt-5.4-mini | OpenAI | Fast, cost-efficient, excellent for sentiment classification |
| gpt-5.4 | OpenAI | Higher quality, good for complex or ambiguous feedback |
| Phi-4 | Microsoft | Strong reasoning, open-weight |

> **Tip:** gpt-5.4-mini is the best choice for this lab -- it is fast, inexpensive, and well-suited for sentiment analysis and classification tasks.

## Step 5: Check model details

The **gpt-5.4-mini** model from Azure OpenAI is high quality, fast, and cost-efficient, which makes it ideal for Caldova's consumer sentiment analysis pipeline.

Find **gpt-5.4-mini** in the catalog and open its detail page. Explore the tabs at the top:

1. **Details** -- Model description and capabilities
2. **Benchmarks** -- Scores and performance metrics
3. **Responsible AI** -- Guardrails imposed on the model from Azure AI Content Safety
4. **License** -- Links to applicable licensing terms

> **Note:** The model card is opened in a web browser page. Make sure to return to VS Code after reviewing it to continue with the lab.

## Step 6: Explore the playground (Optional)

1. Back in VS Code, under **Developer Tools → Build** in the toolkit panel, open the **Model Playground**.
2. Select **gpt-5.4-mini** from the model dropdown.
3. In the **System prompt** (instructions) field, enter:

    ```text
    You are a consumer engagement insight analyst for Caldova, a global pharmaceutical company. Classify the sentiment of the following consumer feedback as POSITIVE, NEUTRAL, NEGATIVE, or MIXED. Respond with only the sentiment label.
    ```
4. In the chat box, enter:

    ```text
    I felt dizzy after taking the Caldova allergy relief tablets.
    ```
5. Send the message and observe the response. This is a preview of the inference pattern you will implement in code during Labs 3 and 4 to analyze sentiment in Caldova consumer feedback.

## What you learned

- ✅ How to navigate the Foundry Toolkit in Visual Studio Code
- ✅ How to browse the model catalog from within VS Code
- ✅ How a model responds to a Caldova consumer sentiment prompt

## Key takeaway

> Microsoft Foundry provides access to production-ready hosted models from multiple publishers. You do not need to train, fine-tune, or host these models yourself -- you simply connect to them via API and start building. For Caldova, this means a working consumer sentiment analysis prototype in hours, not weeks.

---

**Next:** [Lab 2 - Verify your project](./lab2-verifysetup.md)

