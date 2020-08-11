# Banking Simulation

This is the backend server of a banking application which simulates the creation of a bank account. It includes a `Savings` account for each user, and a history of the user's `Transactions`.

### Links

-   [Client Side Repo](https://github.com/kkorrapaty/bank-sim-client)
-   [Deployed API](https://bank-sim-server.herokuapp.com)
-   [Deployed Site](https://kkorrapaty.github.io/bank-sim-client/#/)

## Planning

I started with creating a `Savings` model. It includes an `amount` field that takes a decimal value:
* Minium amount of 50.00
* Max decimal places = 2
* Max digits = 8

and an owner field that connects to the User's Id. After that, I made a `Transactions` model that takes two values:
* the change in amount
* current total after the change

and it has a ManyToOne relationship with Savings.

#### Technologies Used

-   Python
-   Django
-   Postgres

#### Future Additions

In the future versions of this application I would like to add the ability for users to create multiple checkout accounts. As well as that, I want to invoke a functionality that allows those various accounts to transfer funds between each other

****
ERD:

![ERD](https://media.git.generalassemb.ly/user/28548/files/ddd64380-d700-11ea-84f9-d04a79000329)
