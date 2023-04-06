# Accelerate AWS IAM Identity Center operations with Automation
Assigning permission sets to users and groups in AWS IAM Identity Center and grant access for users and groups to multiple AWS accounts in their organization is quite tedious and required many more ClickOps operations.

Considering this fact, I've developed this automation to help customers to perform these permissions set and user/groups association activities without many efforts.

### Tech Stack
1. Python 3.0 or any other version >3.0
2. boto3 to call AWS APIs
3. pandas, numpy and openpyxl libraries to perform Excel sheet operations
4. awsretry - To retry AWS APIs in case of throttling issues

### Walkthrough
This project uses an Excel sheet to source data for mapping permission sets and users/group to an account, organization unit (OU) or all the accounts in an OU. I recommend that you manage the IAM Identity Center identity on the group level as a best practice, every workforce user should be part of a group.
Main steps:

- Step 1: Clone the GitHub repository.
- Step 2: Update CSV file with required data.
- Step 3: Update AWS account details in the program file.
- Step 4: Install Python libraries for program execution.
- Step 5: Execute Python Program.


##### Step 1: Clone the GitHub repository.
Clone the GitHub repository to your local system. This repository contains example data files that you can use to update permission sets and users/groups to account(s). You can modify the example data with your own account IDs or OUs and resource names.

##### Step 2: Update CSV file with required data
This automation use CSV as a source of data and perform Identity center operations accordingly. You can find this CSV in the code at following path
`file/Identity Center Access Management.xlsx`
This CSV contains two worksheets. 
1. **Data** - This is master data of AWS Organization and includes following tables. Please refer following screenshot for your reference

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s0ian28ddyfrwbisob98.png)

Each table has a purpose in this sheet
- **Targets**- Permission sets and users/groups can be associated with either specific `ACCOUNT` or all the accounts in an `OU`

- **OU Name** - Values are in the form `OU_NAME[ORGANIZATION_UNIT_ID]`.

- **ACCOUNTS** - Values are in the form `ACCOUNT_NAME[ACCOUNT_NUMBER]`
- **OPERATIONS**- `Add` or `Update` or `Delete`

2. **Identity Map** - This worksheet provides source data for this automation and accordingly permission sets and users/groups will be associated with AWS accounts on AWS Identity Center
Please refer following screenshot for your understanding.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7e2c0fwgp4pmeu8mea9x.png)

Here is the description to understand this CSV better

- Row 2: Associate permissions set `AWSPowerUser` to user `abcd@example.com` on `Sandbox` OU
- Row 3: Associate permissions set `ReadOnlyAccess` to group `AuditorsGroup` on `Sandbox` account
- Row 4: Associate permissions set `AdministratorAccess` to group `AdministratorsGroup` on `ALL` accounts in an organization except management account of an organization

Let's take another example to understand various functionalities of this automation

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gv8te909tz47emw5sphn.png)

Here is the description of the above snippet to understand this automation much better

- Row 2: Delete association of user `abcd@example.com` and permissions set `AWSPowerUser` from all the accounts in `Sandbox` OU

- Row 3: Delete association of group `AuditorsGroup` and permissions set `ReadOnlyUser` from `Sandbox` account

- Row 4: Associate permissions set `AuditorsPolicy` and group `AuditorsGroup` on `ALL` accounts in an organization except management account of an organization.

>Please note, this program is stateless,
meaning it won't impact any other associations of permission sets and users/groups to AWS accounts.
It just considers data from Excel sheet and perform associations/de-associations accordingly.

**Step 3: Update AWS account details in the program file**
To execute this automation, we have to update AWS resource details in a configuration file. You can find this configuration file in the code at path `config/aws_properties.py`
Please refer following snippet and the comments on each property for your reference

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hzj8cqvqtvunadpono3c.png)

**Step 4: Install Python libraries for program execution.**
To install Python libraries, I've included `requirements.txt`in the code. You can find this file at root location in the source code. We need to install following libraries for successful execution of this program
```
1. boto3
2. pandas
3. awsretry
4. numpy
5. openpyxl
```
Assuming you can run pip command on your system, go to the project root directory and execute following command to install these libraries.

```
pip install -r requirements.txt
```
**Step 5: Execute Python Program**
Assuming that you have right credentials and system requirements to execute this code, update credentials in `~./aws/credentials` file or if you are running it on `Amazon EC2` then make sure that you have IAM role with sufficient permissions associated with the instance
To execute the program, go to root directory of the project and execute following command

```
python local_handler.py 
```

This program prints all the actions performed during execution, and you can expect logs like below

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2dlm6do3gut6ytfpmjtn.png)