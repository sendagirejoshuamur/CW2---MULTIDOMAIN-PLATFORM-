# Week 7: Secure Authentication System

Student Name: Joshua Sendagire  
Student ID: M01045908
Course: CST1510 - CM2 - Multi-Domain Intelligence Platform  

## Project Description

A command-line authentication system implementing secure password hashing using bcrypt. This system allows users to register accounts and log in with proper password verification, ensuring security through industry-standard cryptographic practices.

## Features

- Secure Password Hashing**: Uses bcrypt with automatic salt generation
- User Registration**: Prevents duplicate usernames with proper validation
- User Login**: Verifies credentials against securely stored hashes
- Input Validation**: Comprehensive username and password validation using regex
- File-based Persistence**: User data stored securely in `users.txt`
- Professional CLI Interface**: User-friendly menu system with clear feedback

## Technical Implementation

- Hashing Algorithm**: bcrypt with automatic salting (12 rounds)
- Data Storage**: Plain text file (`users.txt`) with comma-separated values
- Password Security**: One-way hashing, no plaintext storage
- Input Validation**: 
  - Username: 3-20 alphanumeric characters
  - Password: 6-50 characters with uppercase, lowercase, and digit requirements
- Error Handling**: Comprehensive exception handling for file operations