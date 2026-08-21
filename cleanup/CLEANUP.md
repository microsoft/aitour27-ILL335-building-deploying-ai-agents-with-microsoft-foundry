# Clean up Azure resources

Complete this checklist when you finish the workshop to stop charges from resources created for the lab.

> [!WARNING]
> `azd down` can permanently delete the resource group and every resource in it. Confirm the active environment, subscription, and resource group before approving deletion. Do not use this command for a shared environment.

## Cleanup checklist

- [ ] Save any outputs or screenshots you want to keep.
- [ ] Open a terminal in the repository root.
- [ ] Confirm the active Azure Developer CLI environment:

  ```powershell
  azd env list
  azd env get-values
  ```

- [ ] Confirm that the environment belongs to this workshop and does not use a shared Foundry project.
- [ ] Preview the resources that `azd` manages:

  ```powershell
  azd show
  ```

- [ ] Delete resources created by this `azd` environment:

  ```powershell
  azd down
  ```

- [ ] Review the resource list, then approve deletion only when the subscription and resource group are correct.
- [ ] Verify in the [Azure portal](https://portal.azure.com) that the workshop resource group was removed.

If this environment was connected to an existing Foundry project, `azd down` leaves that project and its resource group in place. Remove only the agent versions or model deployments created for this workshop, and coordinate with the project owner before deleting shared resources.

## Local files

The `.env`, `.venv`, and `.azure` directories contain local configuration or generated state and are excluded from source control. You can remove them after the workshop if you no longer need this local environment.

---

**Previous:** [Lab 7: Workshop summary](../docs/lab7-summary.md)