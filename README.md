# book-discount-tracker
A simpler crawler that given a list of books will track down their discounts from Politeia and Protoporia bookshops.

# How to run
- Copy `library.template.json` to a file named `library.json`. This will hold your configuration. Add any books there, using the default template.
- Make sure you have docker installed.
Create a docker image with `docker build -t book-tracker .`
Then run it with `docker run --rm book-tracker`