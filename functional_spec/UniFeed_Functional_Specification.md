# 0. Table of Contents
- [1. Introduction](#1-introduction)
  - [1.1 Overview](#11-overview)
  - [1.2 Business Context](#12-business-context)
  - [1.3 Glossary](#13-glossary)
- [2. General Description](#2-general-description)
  - [2.1 Product/System Functions](#21-productsystem-functions)
  - [2.2 User Characteristics and Objectives](#22-user-characteristics-and-objectives)
  - [2.3 Operational Scenarios](#23-operational-scenarios)
  - [2.4 Constraints](#24-constraints)
    - [Time Constraints](#time-constraints)
    - [Performance Constraints](#performance-constraints)
    - [Scalability Constraints](#scalability-constraints)
    - [Ethical and Legal Constraints](#ethical-and-legal-constraints)
    - [Budgetary Constraints](#budgetary-constraints)
- [3. Functional Requirements](#3-functional-requirements)
  - [3.1 User Account System](#31-user-account-system)
  - [3.2 Email Verification](#32-email-verification)
  - [3.3 Recover Account Password](#33-recover-account-password)
  - [3.4 Import RSS Feed](#34-import-rss-feed)
  - [3.5 Update RSS Feed](#35-update-rss-feed)
  - [3.7 Manage RSS Feed](#37-manage-rss-feed)
  - [3.8 Detect Political Bias](#38-detect-political-bias)
  - [3.9 Create Folder](#39-create-folder)
  - [3.10 Add Feed to Folder](#310-add-feed-to-folder)
  - [3.11 Display Folder](#311-display-folder)
  - [3.12 Manage Folder](#312-manage-folder)
  - [3.13 View Article Details](#313-view-article-details)
  - [3.14 View Recently Read Articles](#314-view-recently-read-articles)
  - [3.15 Add to Read List](#315-add-to-read-list)
  - [3.17 Save Article](#317-save-article)
  - [3.18 Web Scraping Service](#318-web-scraping-service)
  - [3.19 Provide A.I Feedback](#319-provide-ai-feedback)
- [4. System Architecture](#4-system-architecture)
  - [4.1 A.I Component Architecture](#41-ai-component-architecture)
  - [4.2 Web Application Framework](#42-web-application-framework)
  - [4.3 Web Scraping Component](#43-web-scraping-component)
  - [4.4 Third-Party Libraries and Dependencies](#44-third-party-libraries-and-dependencies)
  - [4.5 Ethics and Compliance](#45-ethics-and-compliance)
- [5. High-Level Design](#5-high-level-design)
  - [5.1 System Overview](#51-system-overview)
  - [5.2 Component Architecture](#52-component-architecture)
  - [5.3 Third-Party Integrations](#53-third-party-integrations)
  - [5.4 Data Flow Diagram](#54-data-flow-diagram)
- [6. Preliminary Schedule](#6-preliminary-schedule)
  - [6.1 Project Timeline](#61-project-timeline)
  - [6.2 Project Timeline Gantt Chart](#62-project-timeline-gantt-chart)
  - [6.3 Timeline Milestones](#63-timeline-milestones)
- [7. Appendices](#7-appendices)
  - [Simple UI Mock-up](#simple-ui-mock-up)
  - [Early System Flowchart](#early-system-flowchart)


# 1. Introduction
## 1.1. Overview

### System to be developed
The system UniFeed is a news aggregation app that uses Artificial Intelligence (AI) to detect political bias within news articles. UniFeed is designed to offer a centralized platform where users can import their news feeds from different sources into a convenient one-stop location. 

What makes UniFeed stand out is its A.I feature that detects political bias. This helps to not only promote a more informed reading experience but to enhance the users' understanding of potential biases in the news content that they consume. The system aims to be a valuable resource for anyone who is seeking an informed perspective as it allows them to discern and understand any political bias in their news consumption.

### Key functions
- A Centralized News Platform: UniFeed allows users to aggregate their news sources into a single unified feed. The user can create an account, where they can manage their imported feeds and news articles. 
- A.I Analysis and Bias Detection: The system can run an A.I analysis on news articles. The A.I evaluates the content and provides an estimate of political bias.
- User Reading Analytics: The user can opt to have UniFeed keep track of their various reading habits, which will be displayed in a private dashboard.

### Integration with Other Systems
The system integrates with the RSS (Really Simple Syndication) feed system to allow users to import both custom curations and pre-existing feeds provided by news websites. RSS was released in 1999 so it is well established with an abundance of feeds readily available. This integration not only allows a user to continue using their existing but also ensures that UniFeed can create a broad and varied news aggregation.

## 1.2 Business Context
### 1.2.1 Introduction to Business Context

#### Impact on News Consumption
UniFeed could have a broad impact on the landscape of internet news consumption. It shall offer a modern clean design that appeals to many users as a new home to congregate and read their news feeds. This ensures that UniFeed has a great appeal to regular internet users who consume news content. The system incorporates features that utilize artificial intelligence, positioning it to offer a unique value proposition by revealing political biases in news content. This aspect of UniFeed potentially makes it impactful across many sectors, ranging from media and journalism to education and political analysis. 

#### Demographic Appeal
UniFeed integrates the latest technology trends to provide a system with new features to an already existing demographic. It presents an appealing tool for both general and expert users. The general user demographic ranges from online news consumers seeking a new modern platform to tech savvy users drawn to the artificial intelligence capabilities that will highlight any bias in the media content that they consume. The expert user demographic that UniFeed appeals to includes academics seeking a media analysis tool, as well as political organization and media companies utilizing it as a strategic instrument for crafting their messages and brand. 

### 1.2.2 Business Applications 
#### Journalism and Media Companies
UniFeed can be a tool for companies in the realm of journalism and media to gauge the political bias in their content. This insight can help them adjust their reporting to ensure balanced news coverage. Media companies might use UniFeed to monitor competitors and understand the overall bias landscape in the media industry.

**Example:** an editor for a news organization could import a draft article into UniFeed to classify a political bias on the text content. The results of the classification can provide awareness of any political bias, allowing the editor make decisioned before the content is published onto their news website. 

#### Political Organisations
Political groups can use UniFeed to understand how different news outlets are portraying them or the issues that they care about. It can be used as a strategic tool for crafting communication and public relations strategies that allow their messages to counter any prevailing media biases. 

**Example:** a political advocacy group focused on environmental changes can utilize UniFeed to monitor and track how different outlets report on climate change. They could draw a correlation between different political biases and perspectives on environmental legislation. With the insight, the group could tailor their communication strategies effectively to ensure that their message is impacting the correct demographic.

#### Marketing and Public Relations
UniFeed can assist marketing and PR agencies to better understand the media landscape so that they can tailor their campaigns and public statements. These agencies could use insights from UniFeed to advise clients on where to place advertisements or the type of audience that they will need to frame their public statements or tailor their marketing strategies for.

For public relations, UniFeed can help to highlight any reoccurring biases amongst different news outlets for a greater overview on their existing material. This would allow for an informed strategy when associating clients with different platforms. 

**Example:** a marketing agency representing a health and wellness brand could leverage the system to analyse coverage around different health trends and products. The data from UniFeed could reveal that a particular bias correlates to a different approach to health and awareness—like a focus on natural remedies over pharmaceuticals. The agency can advise their client on how to frame their campaign messaging or product to better align with the demographics.

#### Education
UniFeed can be an educational tool, helping students and educators analyse media bias and further develop their critical thinking skills. The system could help understand the nuances of news reporting and political bias, promoting the development of a greater media literacy. The platform may be used by students to gather data for political biases in media or offer a case study to discuss the use of artificial intelligence and the intersection between technology and media.

**Example:** students in studying a subject where media consumption is highly relevant, such as:  journalism, political science, or media studies can use UniFeed as a research tool for tracking different trends of political bias in online news. UniFeed provides a means to gather new data or use existing bias classifications to analyse the portrayal of specific topics across different news sources.

## 1.3 Glossary

| Term | Definition |
|------|------------|
| **A.I** - Artificial Intelligence | Refers to the simulation of human intelligence in machines programmed to think and learn like humans. |
| **NLP** - Natural Language Processing | A field of artificial intelligence concerned with the interactions between computers and human languages. |
| **RSS** - Really Simple Syndication | A web feed that allows users and applications to access updates to online content in a standardized format. |
| **UI** - User Interface | Anything that a user may interact with to use the system. |
| **Web Scraper** | A tool used to read HTML and XML content from a url.|
| **XML (eXtensible Markup Language)** | A markup language for creating custom data formats, enabling the structured sharing of data across various systems. |
| **HTML (HyperText Markup Language)** | A markup language for creating and structuring sections, paragraphs, and links on web pages. | 
| **GDPR** - General Data Protection Regulation | A regulation in EU law on data protection and privacy in the European Union and the European Economic Area. |
| **Left Wing** | A political viewpoint characterized by an emphasis on ideas such as equality, social justice, environmental protection, and government intervention in the economy. |
| **Right Wing** | A political stance advocating for free market policies, reduced government intervention in the economy, traditional values, and individual liberty. |
| **Centre Leaning** | A political position that involves a balance or blend of left-wing and right-wing policies, often emphasizing pragmatism and compromise. |
| **Political Bias** | A tendency to favor certain politicians, parties, or ideologies over others, often resulting in an unbalanced or partial perspective. |
| **QoL** - Quality of Life (Software Development) | Refers to enhancements in software that improve usability and efficiency. Typically involves modifications or features introduced by developers to simplify processes and enhance the overall user experience. |
| **IDE** - Integrated Development Environment | A software application that provides comprehensive facilities to computer programmers for software development. |

# 2. General Description
## 2.1 Product/System Functions

### User Interface

UniFeed's interface is designed with a modern aesthetic that emphasizes simplicity and ease of use. The layout is clean and uncluttered, using a minimalist design approach to enhance user focus on the main content. To accommodate users with different needs, the design will follow web content accessibility guidelines and implement accessibility features such as screen reader compatibility and tab key navigation. 

The design will  make use of a colour scheme that is carefully selected to be visually appealing while ensuring that the text is easy to read, good contrast ratios are followed, and important elements are sharpened. The user interface shall be responsive, allowing it to adapt seamlessly between different devices and screen sizes allowing for a comfortable reading experience amongst all users. 

### News Aggregation

The system aggregates the articles from multiple RSS feeds into a cohesive singular interface. A user may import an RSS feed by its given URL. UniFeed will read the feed's contents and pull individual articles within. 

The content of all imported RSS feeds will be displayed together on a single page found at `USER_ID/feeds/all`.  Alternatively, the user can organise these feeds into different folders, and subsequently, individual pages. For example: a folder titled ‘Space’ may contain the RSS feed from NASA and SpaceX. This would create a new page: `USER_ID/feeds/space` - which will contain all articles from NASA and SpaceX.

### User Customization

Users can create an account to manage their imported feeds and reading habits. They can flag articles to read later, save their favourite articles, view their reading history, and organise their feeds into different folders. This allows users to have a level of personalization over their interaction with the system.

### AI-Driven Political Bias Detection

UniFeed shall use artificial intelligence to classify the content of articles, and determine a political bias rating. The user can elect to run a political bias analysis on any article within their feed. If they choose to do so, the system deploys a web scraper to extract the content of the article, which is then analysed by the AI. The results are displayed to the user indicating the bias alongside the AI’s confidence with the classification.

### User Analytics

Each user will have an analytics dashboard where they can see details to analyse their reading habits, such as:
- The average number of articles read per day.
- Identification of their favourite news category.
- A calculation of the average political bias across the articles they read.
- Their most frequently visited news sources.
Respecting user privacy and preferences, the analytics shall be provided on an opt-in/opt-out basis.

## 2.2 User Characteristics and Objectives
### General Users
- **Expertise**: Ranging from casual news readers to more tech-savvy individuals. Varied levels of technical proficiency; ranging from basic to advanced. No specific technical skills required for basic usage.
- **Expectations**: Intuitive user interface, easy to use seamless news aggregation, unbiased content analysis, and personalization options.
- **Objectives**: Easily accessible news aggregation and insights into the political bias of their news sources.
- **Example Use Cases**:
	1. **News Aggregation**: A casual user logs in to UniFeed to check the latest news from various sources consolidated into one feed.
	2. **Bias Detection**: A user reads an article and uses the A.I feature to understand its political bias, aiding their understanding of the content.
	3. **Customization**: A user customizes their news feed categories for a more personalized experience.
	4. **Analytics Overview**: A user reviews their reading habits and the average political bias of the articles they've read, using UniFeed's analytics dashboard.

### Expert Users
- **Expertise**: Ranging from journalists and political analysts to academics and students. Higher proficiency in digital media tools and understanding of media bias. Require skills for advanced media analysis and critical evaluation of content.
- **Expectations**: Clear indicators to discern media bias and trends, user analytics for in-depth bias analysis, ability to save A.I classification results, an option to import individual articles for analysis, and feed customization capabilities.
- **Objectives**: Utilize UniFeed for professional or research purposes, such as media analysis, campaign strategy development, or academic research.
**- Example Use Cases:**
	1. **Media Analysis**: A journalist uses UniFeed's advanced analytics to study bias trends across various news outlets.
	2. **Academic Research**: A researcher imports specific articles for detailed bias analysis, exporting the AI's classification results for further study.
	3. **Campaign Strategy**: A political analyst aggregates news related to specific political events or figures, using UniFeed to gauge political bias in the media portrayal.
	4. **Educational Tool**: A media studies teacher employs UniFeed in a classroom setting to teach students about media bias, critical reading skills, and the intersection between technology and media.

## 2.3 Operational Scenarios

### Scenario 1: Daily News Consumption 
* **User Type:** General User
- **Situation**: Michael, a college student, uses UniFeed daily to stay updated with the latest news. He is wary of political bias in media and prefers neutral perspectives.
- **Action**: Michael logs into his account to view his personalized feed. His feed is tailored to his interests in politics and movies. He skims through the most recent articles and comes across a headline that grabs his attention. He clicks to view the article details and chooses to run a political bias analysis. The A.I returns a result indicating  no detectable political bias.
- **Reaction:** Michael feels reassured and confident about the nature of the content within the article
- **Outcome**: Michael decides to read the full article knowing that it aligns with his desire for neutral perspective. 
### Scenario 2: Journalism Application 
* **User Type:** Expert 
- **Situation**: Danielle, an editor at a major news organization, needs to maintain the company's commitment to balanced reporting.
- **Action**: Danielle logs into her account. She imports a private RSS feed that contains URLs to hidden unpublished articles. UniFeed imports the draft articles into its system, where she can check them for any political bias. The A.I analyses the text and provides a bias classification.
- **Reaction**: Danielle finds that an article is skewing slightly towards a political wing.
- **Outcome**: She provides the results to the journalist to adjust the reporting to be more neutral, aligning with the company's commitment and editorial standards.

### Scenario 3: Political Organisation Strategy
* **User Type:** Expert
- **Situation**: Enrique, a campaign strategist for a political party, wants to monitor how different news outlets are covering their campaign.
- **Action**: Enrique signs in to UniFeed. He imports his custom made RSS feed which contains articles pertaining to his political organisation that he has carefully curated.  UniFeed parses these articles into a feed. Enrique decides to go through each article and run the political bias check on them.
- **Reaction**: He discovers a trend in the bias of certain publications that could affect public perception.
- **Outcome**: Enrique advises the campaign on his findings and discusses strategic communication moves to counteract any negative bias.

### Scenario 4: Marketing Campaigns
* **User Type:** Expert
- **Situation**: Willow, a marketing executive, needs to develop a campaign for a client's new product launch.
- **Action**: She uses UniFeed to analyse articles that are highly popular promoting a similar product. She discovers that there is a common trend of political alignment amongst the outlets that speak positively of the product.
- **Reaction**: Willow finds valuable insights about the target audience's leanings and media consumption habits.
- **Outcome**: She tailors the marketing campaign to align with the audience's preferences, increasing the success of the product with its target demographic.

## 2.4 Constraints
### Time Constraints
The functionality of the system must adhere to a strict 3 month development timeline to ensure that its ready in time for the project demonstration. The key milestones of this timeline are:
- Developing the A.I model
- Developing the Web Scraper.
- Designing and implementing the User Interface.
- Integrating the systems together.
- Testing and validating the system.

### Performance Constraints
The system must efficiently handle its primary functions of 
* Importing new data through RSS feeds
* Scraping content from articles
* Classifying political bias text

All of these functions must perform their actions without significant delay (e.g., RSS feed import within 5 seconds, content scraping and bias classification within 10 seconds per article). This is important to ensure that the website functionality feels quick, responsive and offers a good user experience. 

### Scalability Constraints
The system needs to be capable of scaling up to accommodate a growing user base and increasing data volume. The A.I and web scraper must be efficient enough to handle multiple concurrent requests in a reasonable time manner . There needs to be careful consideration when deciding what aspects to store in the database, to ensure that storage size is capable of handling all data as the volume increases.

### **Ethical and Legal Constraints**
UniFeed must accommodate for ethical and legal considerations. Particularly with storing user data, A.I bias detection and content scraping. 

The system will be fully transparent with its A.I classification. UniFeed will provide clear explanations of how the A.I model determines political bias so that users understand the basis of the AI's decisions. The potential inaccuracy of the A.I will be transparent to each user any time a political bias is classified or labelled.

UniFeed will be compliant with data privacy laws such as GDPR. It will involve obtaining user consent for any data processing or tracking. The system will store data with the latest encryption technology and security measures. 

Web scraping will be conducted ethically, respecting copyright laws and the terms of use of the source websites. The system will only scrape content that is publicly available and will not store any content from the source other than metadata.

### Budgetary Constraints
The server costs associated with running a Web Scraper and A.I could prove too great for the scope of the project. It may be the case that functionality will need to be limited globally or on a per user basis. This could mean restricting the frequency of updates, the number of articles analysed per user, or the depth of data scraping (how much of the article content the scraper reads).
# 3. Functional Requirements
## 3.1 User Account System

**Description**
Users can create a personal account by providing a username, their email, and a password. The account will hold data that is crucial for providing a tailored experience to the user such as their:
* Imported RSS feeds.
* Saved articles.
* Personal Reading list.

**Criticality: High**
User accounts are essential for personalization, security, and continuity between sessions.

**Technical Issues**
- Ensuring secure storage for user credentials.
- Guaranteeing data privacy.

**Dependencies With Other Requirements**
- Database: to store, manage, and verify user account information.
- Email Verification: for verifying that the user entered a real email address.
## 3.2 Email Verification
When an users registers an account or attempts to reset their password, they must verify the action with their email address. The functionality of this involves automatically sending the user an email with a verification code or link. When the user clicks the link or enters the code, their email interaction is verified.

**Criticality: High**
Crucial for authenticating a users account and protecting their information from malicious actors. Allows users to reset their password in cases where they lost or forgot it.

**Technical Issues**
- Setting up the automatic email system.
- Seamlessly integrating the verification into the account registration process.
- Ensuring that emails are secure and reliable.
- Implementing a time limit (e.g.,: 1 hour) before invalidating the reset to maintain the security of the process.

**Dependencies With Other Requirements**
- User Account System: email verification is a part of the account creation process.
- Recover Account Password: email verification is a part of the password recovery function.
- Database: Stores the verification codes/links and their associations with user accounts.
## 3.3 Recover Account Password

**Description**
The user shall be able to recover their account if they forgot their password. This process involves verifying the users identity, sending a password reset link to their registered email address, and allowing them to set a new password.

**Criticality: High**
Password recovery is important for maintaining a users ability to access their account and personal information.

**Technical Issues**
- Ensuring the reliability of email delivery for the password reset link.
- Creating a user friendly interface for the password recovery to avoid confusion or frustration.
- Preventing unauthorized password reset attempts.

**Dependencies With Other Requirements**
- Database: to verify user identity and update password information.
- Email Verification: to send password recovery or reset links.
- User Account System: the password recovery is dependent on the existence of a user account.

## 3.4 Import RSS Feed

**Description**
Users can import custom feeds by providing the system with the URL of an RSS feed. This deploys the Web Scraping Service to read XML data from the feed and parse it into the system. Importing RSS feeds allows for users to customize their news feed based on personal interests, preferred news sources, or topics.

**Criticality: High**
Directly impacts user engagement, personalization, and is a centrepiece feature of the system.

**Technical Issues**
- Must consider universal parsing and handling common RSS standards to combat variance when interpreting fields between different RSS feeds. 
- Scalability and performance issues when handling multiple RSS feeds. It is essential to employ a mechanism to cache feeds and avoid importing the same feed multiple times for different users.
- Potential security issues if the user attempts to import a URL that contains invalid or malicious data. The system should have safety mechanisms to ensure that the input is an RSS feed.

**Dependencies With Other Requirements**
- Database: to store imported feed information.
- User Account System: to associate imported feeds with the correct user account.
- Web Scraping Service: to parse XML from the RSS feed.
- User Interface: to provide the ability for the user to trigger Import RSS Feed and to display the imported RSS feed to the user.
## 3.5 Update RSS Feed

**Description**
Maintains existing RSS feeds ensuring that they are regularly updated with their latest entries. It is important that site tracks the latest feed developments to display to the user. The feeds shall be updated each time the user logs in or clicks a refresh button.

**Criticality: High**
Without updating RSS feeds, the site would lose tremendous value since users cannot view the latest news in their feeds.

**Technical Issues**
- Scalability issues will appear as the number of imported RSS feeds increases. Multiple users may attempt to update the same feed, in this case, the system shall be able to avoid redundantly querying the same feed multiple times.
- The reading mechanisms will need to be fine tuned to allow for the quickest update time whilst balancing the impact on system performance.
- The system shall handle issues such as a feed being temporarily, or permanently disabled by employing a retry mechanism. The retry mechanism shall trigger every 2 hours, up to 12 times. If the feed is unreachable after the 12 attempts, the system will consider it "dead". Retries will cease and the user will be alerted.

**Dependencies With Other Requirements**
- Database: to store updated feed information.
- Import RSS Feed: to introduce RSS feeds for the function to manage.
- User Interface: to notify the user of updates, or to display any errors that may occur with the potential volatility of RSS feeds.
- Web Scraping Service: to parse XML from the RSS feed.

## 3.7 Manage RSS Feed

**Description**
The user has the ability to modify or delete an existing feed. Modifying the feed will allow for the user to change the RSS URL, which is particularly useful if the feed changes location and the user wishes to maintain access without losing feed specific settings, such as its folder and associated articles. If the user elects to delete the RSS feed, the action will be accompanied by a prompt to inform the user about the permanent loss of data alongside a confirmation to prevent accidental deletion. 

**Criticality: High**
Essential for housekeeping and long term user satisfaction when engaging with the system.

**Technical Issues**
- Updating User Interface to reflect changes.
- Handling articles belonging to the RSS feed when it is deleted.
- Handling scenarios that arise when a deleted RSS feed was aggregated with other feeds.
- Ensuring that there are no accidental deletions.

**Dependencies With Other Requirements**
- Database: to update or remove feed information.
- Import RSS Feed: to introduce RSS feeds for the function to manage.
- Update RSS Feed: coordination between the features is important to avoid the use of obsolete information.
- User Interface: to notify the user of any changes or actions during the feed management process, including confirmation dialogs and error/success messages.

## 3.8 Detect Political Bias

**Description**
The system will employ a machine learning algorithm to assess and quantify the political bias in the text of selected news articles. This feature will enhance the users understanding of an article and promote informed reading. The algorithm will be trained on a dataset that contains left wing, right wing, and centre leaning sources to ensure a wide political spectrum and accurate classification.

**Criticality: High**
Detecting political bias is one of the systems selling points. It is highly likely to be essential for user satisfaction and a required feature for many users.

**Technical Issues**
- Developing a machine learning algorithm that accurately assesses political bias, which involves training the model on a diverse dataset and fine tuning.
- Some articles may not be political in nature, for example: a fashion article. The feature needs to distinguish these scenarios to prevent the misuse of system resources.
- The algorithm needs to be performant and display the political bias to users with minimal delay.
- Providing the users with easily understandable and transparent information about how the bias was derived to ensure credibility. 
- For better scalability and performance, the classifications will be saved in the database, where they can be associated to articles and fetched to avoid repeat classifications.

**Dependencies With Other Requirements**
- View Article: to retrieve the article that the analysis will be performed on.
- Web Scraping Service: to provide text content for classification.
- Database: to store classification results.
- User Interface: to provide the user the option to perform the bias detection on each article and to display the analysis results to the user in a clear and meaningful way.

**Ethical Considerations**
- Any labelling will come with a warning indicating that it was determined by an A.I and may not be fully accurate. 
- If the confidence rate of the A.I does not pass a specific threshold, the system will provide feedback to the user explaining that the article's bias could not be determined with sufficient confidence.
- The A.I will only classify content and not make any value claims or judgements towards a result.
- The requirement "Provide A.I Feedback" will allow users to provide feedback on the bias detection. This can help in refining the algorithm and addressing potential biases within the A.I itself.

## 3.9 Create Folder

**Description**
Allows for organizing different imported feeds into customizable folders. Users can create new folders to categorize their feeds based on topics, sources, or personal preferences.

**Criticality: Medium**
An important QoL feature for organization and personalization but not a necessity for core functionality of the system.

**Technical Issues**
- Ensuring a user-friendly interface for creating and naming folders.
- Handling potential issues with duplicate folder names.
- Integrating folder creation seamlessly with feed import and management.

**Dependencies With Other Requirements**
- Database: for storing folders and their associations with feeds.
- User Interface: for providing an intuitive and accessible way to create and manage folders.
## 3.10 Add Feed to Folder

**Description**
Users have the ability to categorize their imported RSS feeds into folders. This can be done by selecting an existing folder or creating a new one during the feed import process. 

**Criticality: Medium**
An important QoL feature for organizing feeds, enhancing the overall usability and personalization of the system.

**Technical Issues**
- Ensuring that feeds can be added to or removed from folders without data loss or duplication.
- Updating feed organization in real-time across the user's account.

**Dependencies With Other Requirements**
- Database: to track and update the association of feeds with different folders.
- Import Feed: as categorizing the feed into a folder is relevant after import.
- Create Folder: as this feature is integral to categorizing feeds after their import.

## 3.11 Display Folder

**Description**
Folders will generate subdirectories within the system to display the aggregation of the feeds within a folder. For example, visiting the directory `USER_ID/feeds/Nature` will display all feeds within the "Nature" folder to the user. 

**Criticality: Medium** 
Allows for displaying categorized content, which is a major QoL for users who wish to make use of folder organization for their reading experience.

**Technical Issues**
- Creating automatic routes for retrieval and display of feeds from the database based on folder selection.
- Implementing an intuitive navigation system for accessing different folders.
- Handling empty or deleted folders in the user interface.

**Dependencies With Other Requirements**
- Database: to retrieve the correct feeds associated with each folder.
- User Interface: to provide a clear and effective display of folders and their content.
- Add Feed to Folder and Create Folder: as these features directly influence the content displayed within each folder.

## 3.12 Manage Folder

**Description**
This feature enables users to manage their folders, including renaming existing folders and deleting them. Renaming a folder allows users to update its title to better reflect content or their personal preferences. Deleting a folder removes it from the user's account along with its associated feed categorization, but does not delete the feeds themselves.

**Criticality: Medium** 
Renaming allows for users to adapt their feed to evolving content. Deletion ensures that the user can remove redundant or unused feeds, contributing to the long term user experience.

**Technical Issues**

- Implementing intuitive UI controls for folder renaming and deletion.
- Making sure that that folder name changes are reflected across the entire system without impacting the associated feeds.
- Handling the deletion process to ensure that only the folder is removed and the feeds are retained in the user's account.
- Preventing accidental deletions.

**Dependencies With Other Requirements**

- Database: to update folder names and remove folders as required.
- User Interface: to provide accessible and intuitive folder management options within the platform.
- Add Feed to Folder and Create Folder: since managing folders directly affects how feeds are categorized and displayed.
- Display Folder: updating the feed name or deleting the feed should be reflected in changes to the display folder content and route.

## 3.13 View Article Details

**Description**
Allows for users to view the details of the articles gathered from their feed. Article details will appear as a list item in a feed presented in chronological order from the articles publish date. If the user clicks on one of the list items, a modal will appear with the article details.

**Criticality: High**
A feature that will be expected by all user demographics. It is a core functionality of the system. 

**Technical Issues**
* Handling articles that are removed from the UniFeed system or the source news website.
* Presenting all the details and interactive features in an intuitive manner to the user

**Dependencies With Other Requirements**
- Import RSS Feed: as the existence of articles depends on the import of RSS feeds.
- Database: to retrieve article data.
- User Interface: to display the article details and functionality.
- User Account: to track and store user-specific interactions with the article details.

## 3.14 View Recently Read Articles

**Description**
Allows users to access a list of articles they have recently read. When a user clicks to view a full article, it will be automatically added to their reading history. Users can then view a "Recently Read" feed that displays a chronological list of these articles.

**Criticality: Low**
A QoL feature that provides users an easy way to revisit previously read content. Enhances the user experience and allows for greater user analytics, but not necessary for the core functionality of UniFeed.

**Technical Issues**
- Implementing a system to accurately track and record the articles a user reads without impacting system performance.
- Managing the storage and retrieval of reading history.
- Designing an interface for the "Recently Read" feed that seamlessly integrates with the rest of the platform.
- Ensuring privacy and security of the user's reading history.

**Dependencies With Other Requirements**
- View Article Details: as this feature is dependent on identifying which articles a user has viewed to populate the reading history.
- Database: to store and retrieve details of the recently read articles.
- User Account System: to associate the reading history of each user with a persistent account.
## 3.15 Add to Read List

**Description**
Allows users to add an article to a personal "Read List" for future reference. When browsing article details, the user will have the option to add it to this list. This is useful for when the user wants to engage with a particular article but at a later point in time.

**Criticality: Low**
A convenience feature that enhances the user experience. It provides value by allowing users to create a list of future reading material for leisurely or academic reasons. This feature is not essential to the core functionality of UniFeed

**Technical Issues**
- Handling scenarios where articles on the read list are deleted or become unavailable.

**Dependencies With Other Requirements**
- User Account System: to track and maintain a read list for each user.
- Database: to store articles in a users read list
- View Article Details: to give context to the article being added to the user's Read List.
- User Interface: to display the option to add an article to the Read List and the contents of the read list.

## 3.17 Save Article

**Description**
Allows users to save an article that they wish to archive. For example if someone read an article they really enjoyed they could add it to their saved articles to show their friend at a later day.

**Criticality: Low**
Improvement to user experience but a non essential function for the core operation of UniFeed.

**Technical Issues**
- Handling saved articles from deleted feeds
- Handling articles where the source has been hidden or removed
- Providing a page where the user can view all their saved articles

**Dependencies With Other Requirements**
- Database: to store articles that users wish to save.
- User Profile: to ensure saved articles are linked to the right user.
- View Article Details: to choose what article to save
## 3.18 Web Scraping Service

**Description**
The service can fetch XML or HTML data from a given URL. Primarily used to read RSS feed imports and the content of a given article. The scraper needs to be dynamic and capable of handling different structures, layouts, and well handle errors well for scenarios such as a URL containing no content.

**Criticality: High**
Essential for the core system functionality. The Web Scraping Service is required to read RSS feeds and news articles.

**Technical Issues**
Handling scenarios where the data in the URL is unavailable or corrupted.
Being flexible enough to parse websites of many different formats.
Handling inevitable errors that arise when scraping unpredictable content.

**Dependencies With Other Requirements**
- Database: to store scraped content.
- User Account: to associate scraped articles with user requests.
- Import RSS Feed and Detect Political Bias: to provide use cases for the service.
## 3.19 Provide A.I Feedback

**Description**
This feature allows users to give feedback on the AI's bias classification accuracy. When a user disagrees with the AI's assessment, they can submit their perspective, which the system records for review. This feedback loop is crucial for the continuous improvement of the A.I model.

**Criticality: Medium**
Feedback is essential for refining A.I accuracy but is not a core system function like news aggregation or bias detection.

**Technical Issues**
- Implementing an intuitive feedback mechanism that is easy for users to use and understand.
- Handling potentially large volumes of feedback data.
- Ensuring the security and anonymity of user feedback to maintain privacy.

**Dependencies With Other Requirements**
- Database: to store feedback from users.
- User Account: to authenticate and track user submitting feedback.
# 4. System Architecture
## 4.1 A.I Component Architecture

### Overview
UniFeed utilizes artificial intelligence to classify news articles with a political bias rating. The content of the articles will be passed to the A.I from the Web Scraper function. To develop the A.I we will make use of the leading A.I community platform: HuggingFace. The website provides many open source libraries, models, and data sets. HuggingFace's libraries provide a relatively low entry barrier for working with highly performant state-of-the-art machine learning models. 

### Machine Learning Framework
- TensorFlow shall be utilized to build and train the A.I model for predicting political bias. 
- TensorFlow is a highly popular framework for machine learning due to its flexibility, scalability, extensive online resources, community support, and documentation.
- DistilBERT (from HuggingFace's `tansformers` library) will be used as the A.I model for classifying political bias in text due to its its balance between high performance and efficiency.

### A.I Dataset
- The model will make use of the [PoliticalBias_AllSides.txt](https://huggingface.co/datasets/valurank/PoliticalBias_AllSides_Txt) dataset, which contains approximately 20,000  articles from the [AllSides](https://www.allsides.com/unbiased-balanced-news) website. Each article is categorized as 'left', 'right', or 'centre', aligning well with UniFeed's requirement for political bias detection. 
- AllSides Technologies Inc. is renowned for its commitment to presenting a balanced political perspective. The use of their dataset ensures a representative sample for training the A.I model.
- HuggingFace's `datasets`library will be utilized for loading the dataset.
- The dataset will be pre-processed to ensure correct labelling and split into portions for validation.

### Model Training and Evaluation
- The `Trainer` class from HuggingFace will be used to manage the training process.  
- `TensorFlow` will be utilized for model computations.
- `AutoTokenizer` from Hugging Face will be used for DistilBERT compatible text data pre-processing.
- 80% of the dataset will be used for training and the remaining 20% will be reserved for validation.
- Evaluation metrics such as: accuracy, precision, recall, and F1 score will be used to assess the model performance. 
### AllSides Dataset Count Plot

![[diagrams/DATASET.png]]

Count plot of articles within the AllSides dataset.  Generated with pandas - Python Data Analysis Library
### Development Environment and Tools
- Google Colab will be used for access to GPUs specialized in model training, and collaborative features.
- Jupyter Notebooks shall be used due to their ease of use, segmented code, and capability to render visualizations such as graphs to aid in the evaluation of the models performance.
## 4.2 Web Application Framework

### Overview
The UniFeed Web Application is designed to meet four primary requirements:
1. A robust backend that can easily integrate with the A.I and Web Scraper.
2. A secure database that performs and scales well.
3. A well designed interface that implements UniFeed's user interface requirements.
4. A modern responsive frontend implementation.
### Designing the Web Application Interface
Figma will be used for designing the UniFeed interface. Figma is a leading framework for interface design, it has an abundance of resources, user created plugins, and a large online community. The platform contains prototyping tools which will allow us to create an interactive prototype without needing to write any HTML, CSS, or JavaScript allowing different designed to be iterated through with ease.
### Developing the Web Application
UniFeed will be developed using Django as the framework of choice. It is a modern framework that encourages rapid development and takes care of a lot of the heavy lifting so that focus can be shifted onto other aspects of the system. Django allows for an implementation of the unique features and requirement of UniFeed without getting bogged down on reinventing the wheel. Git will serve as the tool for collaboration and version control.

### Key Features of Django Implementation
**Backend** 
Django uses Python, as does the A.I and Web scraping frameworks of choice. This coherence allows for trivial integration between the systems and a consistent development environment. It keeps the stack homogeneous and simplifies development. Django comes with a built in account system and admin interface that will be used for administration, user account handling, and system monitoring.

**Database** 
To fulfil UniFeed's requirements, a database that is both secure and scalable is required. Django comes with SQLite by default, which has proven itself to be more than capable for a project of this scale. If the need for a new solution arises from scalability issues, Django provides the option to easily switch to PostgreSQL or MySQL, ensuring that the application is future proof.

**Frontend** 
Django is weaker on the frontend side, it has basic capabilities that are suitable only for simple interfaces. In UniFeed's case, the user interface requirements are quite minimalistic. Django's frontend capabilities should be sufficient to fulfil the requirements. In the case that a more advanced frontend framework is required, Django has the capability to transition to integrate a different frontend framework such as React whilst still retaining the Django backend. 

### Web Application Testing and Evaluation
Throughout the development of the Web Application, there  will be constant testing and evaluating each iteration.  Selenium shall be used for testing the frontend and ensuring that user interface is functioning as expected. For testing API calls, Postman is the tool of choice. Django has a built in `unittest` library that will be taken advantage of as the main Unit testing suite. For CI/CD pipeline testing, Jenkins will be used.

### Development Environment and Tools
The IDE Visual Studio Code will be used to develop the Web Application Framework. Visual Studio Code has a Django plugin with over 8 million installs, indicating the IDE as a popular choice for the Django framework.

The main software and frameworks we will use for developing the Web Application are:
- Selenium
- Figma
- Postman
- Jenkins
- Django
- Git

The primary languages that we will use during development are:
- Python
- HTML
- CSS
- JavaScript
- SQL

## 4.3 Web Scraping Component
### Overview
An integral part of UniFeed's functionality is its ability to aggregate and process content from various news sources. To achieve this, we utilize a web scraping component built with BeautifulSoup, a Python library designed for parsing HTML and XML documents. This component is responsible for reading RSS feeds by treating them as XML and extracting article content from the HTML of their web page. The article content is then analysed for political bias by the A.I system.

### Key Features of BeautifulSoup Implementation
1. **Content Extraction**: BeautifulSoup is adept at navigating and searching the parse tree of web pages, enabling us to extract relevant content such as article text, titles, and metadata from different news sources. Utilizing BeautifulSoup's parsing capabilities to handle various HTML/XML structures, ensuring consistent and accurate data extraction.
2. **Handling Various Formats**: Given the variety of news websites, each with its unique HTML structure, BeautifulSoup's flexibility allows for handling different page layouts and structures by adjusting different scraping rules and parameters. It also comes with functions for implementing error handling to manage issues such as broken links or access restrictions. 
3. **Integration with Django Backend**: The web scraper works in tandem with the Django backend, feeding extracted data from articles to the A.I component for analysis and storing results in the database.
4. **Tried and True**: BeautifulSoup released nearly 20 years ago, it is still to this day one of the most popular web scraping tools. The python package beautifulsoup4 receives over 16 million weekly downloads. This indicates that the package is widely popular for many use cases, with a rich history of honing for nearly 2 decades.

## 4.4 Third-Party Libraries and Dependencies
### Overview
In the development of UniFeed, across all three main components, several third-party libraries and dependencies play important roles in enhancing the system’s functionality. Many of these libraries are essential for ensuring the systems robustness, and speeding up the development process.

### Key Libraries and Their Roles
1. **[Hugging Face Transformers and Datasets](https://huggingface.co/docs):** Central to the A.I component, Hugging Face provides the DistilBERT model used for classifying political bias in text. The `datasets` library from Hugging Face is crucial for accessing and pre-processing the `PoliticalBias_AllSides.txt` dataset.

2. **[TensorFlow](https://www.tensorflow.org/):** Used for building and training the A.I model within the A.I Component Architecture. TensorFlow Provides tools and libraries to be used for machine learning computations and model training processes.

3. **[BeautifulSoup](https://pypi.org/project/beautifulsoup4/#:~:text=Beautiful%20Soup%20is%20a%20library,and%20modifying%20the%20parse%20tree.):** The core library for the Web Scraping Component, enabling efficient parsing and extraction of web content. The library assists with handling different HTML formats across news source websites.

4. **[Django](https://www.djangoproject.com/):** The primary framework for the Web Application Framework, responsible for both the backend and frontend.

5. **[SQLite](https://www.sqlite.org/index.html) / [PostgreSQL](https://www.postgresql.org/) / [MySQL](https://www.mysql.com/):** Initially, SQLite serves the project needs with the safety net of being able to shift to PostgreSQL or MySQL if any scalability or performance issues arise. 

6. **[Figma](https://www.figma.com/):** Utilized for designing the UniFeed interface, offering a platform for prototyping and iterating design concepts.

7. **[Selenium](https://www.selenium.dev/) and [Postman](https://www.postman.com/):** Selenium is used for automated frontend testing, ensuring UI/UX consistency. Postman assists in API testing.

8. **[Jenkins](https://www.jenkins.io/):** Employed for implementing CI/CD pipelines, automating testing, and deployment processes.

9. **[Visual Studio Code and Its Django Plugin](https://code.visualstudio.com/):** Visual Studio Code is the chosen IDE for its robust support for Python and Django plugin which enhances development productivity with features tailored specifically for Django.

10. **[Git](https://git-scm.com/):** Git serves as the version control system, an essential backbone for collaboration and code management.
## 4.5 Ethics and Compliance
### A.I Transparency
The A.I model developed using HuggingFace and TensorFlow, will have its functionality documented and made transparent. This includes the methodologies used for training and the criteria for political bias classification. Whenever the A.I classifies text, it will make its confidence rate visible to the user. The user can provide feedback on the classification to ensure that the A.I is operating expectantly. This is to build trust with users and provide assurance of unbiased A.I analysis. In

### Compliance with Data Privacy Laws
UniFeed will implement data protection measures to comply with GDPR and other relevant privacy regulations. This will include encrypted storage of personal data, secure handling of user information, and clear privacy policies detailing user data usage (e.g., user preferences, reading history). When the system gathers user analytics, it will be on an opt-in basis with clear indicators of the type of data being gathered.

### Ethical Web Scraping Practices
The web scraping component will be designed to operate within ethical boundaries including respecting robots.txt files and avoiding excessive requests that might overload source websites. It will respect copyright limitations and will not engage in malicious practices. Any article scraped must be publicly available content. The contents of the article itself will not be displayed or stored anywhere in the UniFeed system, only the metadata of the article and its URL. 

# 5. High-Level Design
## 5.1 System Overview
UniFeed will be a web-based application providing news aggregation and political bias detection. The system will be built using the Django framework, with a responsive front-end designed and prototyped in Figma.
## 5.2 Component Architecture

- **Frontend:** Developed using HTML, CSS, and JavaScript. It will offer an intuitive UI for user interactions, such as account management, feed customization, and bias analysis results display.
- **Backend:** Django will handle server side logic, including user authentication, RSS feed processing, and database interactions.
- **Web Scraper:** Built in Python with the BeautifulSoup library. This component is responsible for extracting articles from news feeds and the text from an article's web page. 
- **AI Module:** A separate component using TensorFlow and libraries from Hugging Face for political bias detection. This module processes text from scraped articles and assigns bias ratings.
- **Database:** A relational database for storing user data, imported feeds, and A.I analysis results.
## 5.3 Third-Party Integrations

- **BeautifulSoup** For parsing RSS feeds and news article content.
- **TensorFlow:** For implementing the machine learning model.
- **HuggingFace:** For datasets and A.I model libraries.
## 5.4 Data Flow Diagram
### Level 0

![[diagrams/DFD0.png]]
### Level 1

![[diagrams/DFD1.png]]
# 6. Preliminary Schedule
## 6.1 Project Timeline
### Overview
Our preliminary schedule features 3 distinct phases concurrently across a 4 month period.
* Phase 1: Planning, Writing and Design
* Phase 2: Development and Implementation
* Phase 3: Testing and Validation

### Phase 1: Planning, Writing, and Design

|Task                             | Start      | End      |
|---------------------------------|------------|----------|
|Dataset Analysis and Preparation | Week 1     | Week 1.5 |
|Research Suitable A.I Models     | Week 1     | Week 3.5 |
|Functional Specification Document| Week 1     | Week 5   |
|Competitive Analysis             | Week 1     | Week 5   |
|Select Best A.I Model            | Week 5     | Week 6   |
|Database Design                  | Week 5     | Week 7   |
|Website Design Using Figma       | Week 9     | Week 12  |
|User Manual                      | Week 9     | Week 12  |
|Technical Specification          | Week 12    | Deadline |

### Phase 2:  Development and Implementation

|Task                                         | Start      | End      |
|---------------------------------------------|------------|----------|
|Prototyping of A.I Models                    | Week 2.5   | Week 5   |
|Initialize Django Project Framework          | Week 5     | Week 6.5 |
|A.I Implementation, and Training             | Week 6     | Week 12  |
|Web Scraper Development                      | Week 6     | Week 9   |
|Implement User Registration and Login System | Week 7     | Week 9   |
|Implement RSS Feed Reader                    | Week 7     | Week 9   |
|Implement Feed Folders                       | Week 9     | Week 11  |
|A.I, Web Scraper Integration                 | Week 11    | Week 12  |
|Implement QoL Features                       | Week 11    | Week 12.5|
|A.I System, RSS Feed Integration             | Week 12    | Week 13  |
|Frontend Development                         | Week 13    | Deadline |
|Feedback Collection System                   | Week 13.5  | Week 15  |

## Phase 3: Testing and Validation

|Task                         | Start      | End      |
|-----------------------------|----------- |--------- |
| Initial A.I Model Testing   | Week 2.5   | Week 6.5 | 
| Unit Testing                | Week 7     | Deadline |
| Integration Testing         | Week 7     | Deadline |
| A.I Model Refinement        | Week 7     | Week 9.5 |
| Final A.I Model Validation  | Week 10    | Week 13  |
| UI Testing                  | Week 12    | Deadline |

## 6.2 Project Timeline Gantt Chart
![[diagrams/GANTT_CHART.png]]

## 6.3 Timeline Milestones

- Completion of Functional Specification Document.
- Final selection of A.I Model.
- Completion of A.I training.
- Complete of Website Design.
- Successful Integration between A.I System (AI + Web Scraper) and RSS feed reader.
- Final A.I Model Validation
- Technical Specification completed.
- Completion of Frontend Development.
# 7. Appendices

## Simple UI Mock-up

![[diagrams/UI_MOCK.png]]

## Early System Flowchart

**![[diagrams/FLOWCHART.png]]**