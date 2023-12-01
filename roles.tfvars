custom_roles = [
  {
    name        = "dev-storage-account-contributor-role",
    scope       = "/subscriptions/210990jdf09jfd0",
    description = "Lets you manage storage accounts, including accessing storage account keys which provide full access to storage account data.",
    "actions": [
      "Microsoft.Authorization/*/read",
      "Microsoft.Insights/alertRules/*",
      "Microsoft.Insights/diagnosticSettings/*",
      "Microsoft.Network/virtualNetworks/subnets/joinViaServiceEndpoint/action",
      "Microsoft.ResourceHealth/availabilityStatuses/read",
      "Microsoft.Resources/deployments/*",
      "Microsoft.Resources/subscriptions/resourceGroups/read",
      "Microsoft.Storage/storageAccounts/*",
      "Microsoft.Support/*"
    ],
    "notActions": [],
    "dataActions": [],
    "notDataActions": []
    assignable_scopes = ["/subscriptions/210990jdf09jfd0"]
  },
  {
    name        = "dev-redis-cache-contributor-role"
    scope       = "/subscriptions/210990jdf09jfd0",
    description = "Lets you manage Redis caches, but not access to them.",
    "actions": [
      "Microsoft.Authorization/*/read",
      "Microsoft.Cache/register/action",
      "Microsoft.Cache/redis/*",
      "Microsoft.Insights/alertRules/*",
      "Microsoft.ResourceHealth/availabilityStatuses/read",
      "Microsoft.Resources/deployments/*",
      "Microsoft.Resources/subscriptions/resourceGroups/read",
      "Microsoft.Support/*"
    ],
    "notActions": [],
    "dataActions": [],
    "notDataActions": []
    assignable_scopes = ["/subscriptions/210990jdf09jfd0"]
  }
]


