# Troubleshoot [System or feature name]

This guide helps you diagnose and resolve common problems with [System name]. Each section names a symptom, its cause, and the steps that fix it.

## First checks

Before you investigate a specific error, confirm the basics:

1. Check the installed version:
   ```bash
   [tool-name] --version
   ```
2. Check the [status page](https://status.example.com) for ongoing incidents.
3. Confirm that outbound traffic on ports `443` and *`PORT`* is allowed from your network.
4. Collect the logs with debug output turned on:
   ```bash
   [tool-name] logs --level=debug
   ```

## [Symptom 1 in sentence case, for example: Connection times out during the database handshake]

### Symptoms

- The client prints `Error: ETIMEDOUT connect 192.0.2.1:5432`.
- Requests fail after 30 seconds.

### Cause

The database firewall blocks ingress traffic from your client's IP address.

### Resolution

To allow your client's IP address:

1. Find your public IP address:
   ```bash
   curl https://checkip.example.com
   ```
2. In the console, go to **[Product] > Instances > Connections**.
3. Under **Authorized networks**, click **Add network**.
4. In the **Network** field, enter your IP address in CIDR notation, for example `192.0.2.15/32`.
5. Click **Save**. The change takes effect within a minute.

## [Symptom 2 in sentence case, for example: Requests return 403 Forbidden]

### Symptoms

- The API returns `403 Forbidden`.
- The response body contains `"error": "PERMISSION_DENIED"`.

### Cause

The service account lacks the role that the operation requires.

### Resolution

To grant the role:

1. Find the service account email address in the error log.
2. In the console, go to **IAM & Admin > IAM**.
3. Find the service account and click **Edit**.
4. Click **Add another role** and select **[Required role]**.
5. Click **Save**. Permissions propagate within a few minutes.

## Get more help

- Open a ticket on the [support portal](https://support.example.com).
- Ask in the [developer community forum](https://community.example.com).
