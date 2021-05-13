# online-computer-store-project
# Django Notes

Install These:
  - pip install Django==2.5.2
  - pycharm


Register your completed model in admin.py

	- python manage.py makemigrations
	- python manage.py migrate
	
	
If you're finished, run

	- python manage.py runserver
  
	or 
  
	- Click on run button in pycharm
If there is no superuser, run the command 

	- python manage.py createsuperuser

Also,


Creating a “models” (this creates database tables) Go to models.py Django’s official website is a great and easy resource https://docs.djangoproject.com/en/2.1/ref/models/


# Checklist

Main features of the system:
- [x] 1. The online store has a homepage showing 3 suggested systems chosen by a store manager and 3 most popular computers per number of sales.
- [x] 2. The system provides choices of OS (e.g., win, mac, linux), main purpose (business, scientific computing, or gaming), and architecture (e.g., intel, arm) for the customer to choose from, a new page associated with the choices for different parts, such as cpu, gpu, ram, hard disk, battery, screen, software with possible constraints (a more powerful gpu needs better battery, gaming purpose needs better gpu/screen resolution etc.), and the prices, voting, discussions about each item (if available)
- [x] 3. A visitor can browse the listings of the computer and parts and discussion forums
- [x] 4. A visitor can apply to be a registered customer with a unique working email address, the system maintains a “avoid” list of email addresses, any application whose email address is in this list will be denied and send a denial message to the address, any future applications will be denied without reply.
- [x] 5. A registered customer must provide a working credit card or deposit money to the account for possible purchase.
- [x] 6. A registered customer can browse the system, make purchase options, search info, browse his/her own private purchasing history/expenses, comments and (start) votes on the items s/he purchased already. A customer can buy one whole computer or just a part, can discuss with other of customers or the store clerks.
- [x] 7. At submission of purchase decision, the amount will be checked against the customer’s account or credit, if not enough money, the submission is returned with warning message. If ok, the amount will be charged. The system then puts the purchase to the delivery subsystem.
- [x] 8. There are at least 2 delivery companies that will bid on each item available in the delivery subsystem, a store clerk chooses one based on the bidding. If the winning company’s bidding price is not the lowest, the clerk should provide justifications about her/his choice, otherwise the system will generate a warning on the clerk for possible cheating and shown to the manager.
- [x] 9. The delivery company should provide tracking information for the customer to know its whereabouts.
- [x] 10. A registered customer has an account in the system with information such as available money/credit, home address, purchased computer/items history, and complaints s/he received and filed, votes s/he casted.
- [x] 11. A registered customer can complain about the purchased items, clerks and delivery companies s/he dealt with, which are available to the store managers and the complained clerks/companies/delivery, who should counter with their side of info to clear the warning, the manager can decide to let the warning stay or removed and informing all parties with his/her justifications. A clerk, computer and delivery company that received 3 standing warnings is suspended by the system automatically, the parts of the suspending computer companies and the bidding right of the delivery companies are suspended from the store as well. A customer whose complaint is reversed will receive one warning. A thrice warned customer is removed from the system and put in the “avoid” list. The store manager has the power to remove any customer and clerk with justifications, even with less than 3 warnings. A suspended customer will be informed by email and given the last chance to clean up his/her account.
- [x] 12. In the discussions forum, customers can complain about other customers if they find violating words/sentences/attitude which will be again determined by the manager to stay or reverse as Item 11, or the customer used words that are in the “taboo” list maintained by the clerk/manager, one such violation will automatically generate one warning and the violating words are redacted by *.
- [x] 13. Each team must have one creative feature counted as 10% of the final system to showcase your idea on what ideal feature this store should have. A super creative feature will receive a complimentary bonus (but <=10%).


Other constraint:
1.	You can use real computer (parts) or imaginary ones, which won’t affect your grades
2.	No need to use database as the number of customers and companies are small, a plain text file will do
- [x] A system GUI is required and could be a local desktop app, a web or smartphone system is not required, could be counted as creative feature if you do, but you are warned for its potential technical complexity that may arise.


