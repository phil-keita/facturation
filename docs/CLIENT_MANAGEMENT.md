# Client Management Feature

## Overview

The client management system helps you track your medical office clients and automatically populate receipt information for recurring payments.

## Client Information Tracked

- **Name**: Client's business name (e.g., "Cabinet Dr. Dupont")
- **Type**: Type of medical office (e.g., "Cabinet dentaire", "Cabinet médical")
- **Address**: Full address as a single string
- **Start Date**: When you started working with the client
- **Installation Fee**: One-time setup fee charged
- **Monthly Payment**: Recurring monthly amount
- **Status**: Track client status (Active, Pending, Stopped)
- **End Date**: When the relationship ended (optional)

## How to Use

### Adding a New Client

1. Log in as admin
2. Navigate to **Admin** → **Clients** tab
3. Fill in the "Add Client" form
4. Click "Add Client"

### Managing Existing Clients

- **Edit**: Click "Modify" button next to any client
- **Delete**: Click "Delete" button (requires confirmation)
- **View**: All clients are displayed in the table with their key information

### Using Clients in Receipts

1. Go to **Receipt** page
2. Select a client from the "Select Client" dropdown
3. The form will auto-populate:
   - Client name
   - Payment type (set to "Recurring Monthly")
   - Price (set to monthly payment amount)
4. Adjust any fields as needed
5. Generate the receipt

This saves time when creating monthly recurring receipts for your regular clients!

## Database Migration

If you're upgrading from a previous version without client management:

```bash
python scripts/migrate_add_clients.py
```

This will add the `client` table to your existing database without affecting receipts or expenses.

## Future Enhancements (Suggestions)

Consider adding these features in the future:

1. **Automatic Receipt Generation**: Schedule monthly receipts automatically for active clients
2. **Client History**: View all receipts generated for a specific client
3. **Payment Reminders**: Track unpaid invoices and send reminders
4. **Client Notes**: Add custom notes or special instructions per client
5. **Contract Upload**: Attach PDF contracts or agreements to client records
6. **Email Integration**: Send receipts directly to client email addresses
7. **Payment Status Tracking**: Mark individual months as paid/unpaid
8. **Revenue Forecasting**: Project income based on active client monthly payments
9. **Client Categories/Tags**: Group clients for better organization
10. **Export Client List**: Download client data as CSV/Excel

## API Endpoint

A JSON API endpoint is available for programmatic access:

```
GET /api/clients/<client_id>
```

Returns client details in JSON format. Requires authentication.

## Tips

- Keep the **Status** field updated (Active/Stopped) to ensure only current clients appear in the receipt form dropdown
- Use the **Type** field consistently (e.g., always write "Cabinet dentaire" the same way) for easier filtering in the future
- The **End Date** is optional but useful for record-keeping when a client relationship concludes
- **Monthly Payment** is the most important field for auto-filling recurring receipts
