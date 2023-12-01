# Terraform AI

A simple bot that leverage openapi's assistant API to make changes on terraform tfvars file.

## Setup

Setup venv and activate
```
pip3 install virtualenv
virtualenv .venv
source .venv/bin/activate
```

Install dependencies

```pip3 install -r req.txt```

Export the OPENAI API KEY

```export OPENAI_API_KEY="KEY"```

Run
```
python3 assitants.py
```

Deactivate venv

```deactivate```
