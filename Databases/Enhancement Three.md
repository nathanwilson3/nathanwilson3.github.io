# Artifact Three: Databases
The artifact I selected for my ePortfolio to demonstrate my skills in databases is a dashboard application designed for managing and analyzing data from an animal shelter. This application, originally created as part of my coursework in CS 340 Client/Server Application, interacts with a MongoDB database to perform various operations, including data storage, retrieval, updating, and deletion (CRUD). The application also supports complex queries to filter and analyze the shelter’s data, making it an ideal project to showcase my database management skills.

## Justification for Inclusion
I included this artifact in my ePortfolio because it exemplifies my proficiency in database design, management, and optimization. The project required not only setting up and managing a MongoDB database but also optimizing the database to handle large volumes of data efficiently. I focused on improving the database's performance through the implementation of indexing, optimized queries, and bulk operations. These enhancements demonstrate my ability to design and manage databases that are both scalable and efficient, meeting the needs of real-world applications.

![Dash app 1](https://github.com/nathanwilson3/nathanwilson3.github.io/blob/main/Databases/Dash%20app%20screenshot%201.png)

## Course Objectives Met
The enhancements made to this artifact align with the course objectives related to databases. Specifically, this project demonstrates my ability to implement and manage a NoSQL database (MongoDB) effectively, ensuring that the database can handle large datasets and complex queries. By optimizing the database’s performance through indexing and query optimization, I demonstrated a strong understanding of database management principles and best practices. These improvements are critical in ensuring that the application can scale with the increasing amount of data it needs to manage.

## Process and Learning
The process of enhancing this artifact involved several key steps focused on optimizing the database. Initially, I conducted a thorough review of the existing database structure and identified areas for improvement. One of the first enhancements was the implementation of indexing strategies to improve query performance. By creating indexes on frequently queried fields, such as animal_id and breed, I was able to significantly reduce query times, which is essential when dealing with large datasets.

![Dash app graph and map](https://github.com/nathanwilson3/nathanwilson3.github.io/blob/main/Databases/Dash%20app%20screenshot%202.png)

Additionally, I optimized the application’s data retrieval processes by implementing projections in the queries. This approach allowed the application to fetch only the necessary fields from the database, reducing the amount of data transferred and improving overall performance. I also incorporated bulk operations to handle large data updates and deletions more efficiently, further enhancing the database's performance and scalability.

One of the challenges I encountered was balancing the trade-offs between read and write performance when implementing indexing. While indexes significantly improve read performance, they can also slow down write operations due to the additional overhead of maintaining the indexes. This experience taught me the importance of carefully considering the specific needs of the application when designing and optimizing a database.

![Single and Compound Indexes](https://github.com/nathanwilson3/nathanwilson3.github.io/blob/main/Databases/single%20and%20compound%20indexes.png)


Through this process, I gained a deeper understanding of database optimization techniques and the impact they can have on an application’s overall performance. The enhancements made to this artifact demonstrate my ability to manage and optimize databases effectively, making this project a valuable addition to my ePortfolio.

![Bulk Operations](https://github.com/nathanwilson3/nathanwilson3.github.io/blob/main/Databases/Bulk%20Update%20operation.png)

## Database Repository
[Database](https://github.com/nathanwilson3/nathanwilson3.github.io/tree/main/Databases)
