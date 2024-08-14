# Risk Register

## Sediment Colour as a Record of Climate Change

CITS3200 Group 20  
2024  
University of Western Australia

## Overview

We created this risk register to document potential risks and how they may affect our project's viability. It outlines potential mitigation strategies to reduce the probability of these risks becoming real issues. 

We have identified two risk categories for this project \- technical and project management. Technical risks concern the functioning of specific systems in our project’s software and whether they deliver the necessary and expected outcomes. Risks that fall into this category include incorrect data processing and error reporting. Alternatively, project management risks relate to organisation, communication and planning. Many suggested mitigation strategies relate to project management theory and adopting Agile software development methodologies correctly. 

Identifying and documenting these risks and implementing their mitigation strategies increases the likelihood of successful project delivery to the client. 

## Technical Risks

The technical risks to the project reflect risks that, if not identified, may cause issues even if the project is effectively managed. Many of these risks arise from fulfilling technical requirements in a limited or non-functional manner. These risks may result in poor user experiences and a project that meets requirements in theory but falls short of the client’s expectations in reality. Some risks also arise from simply incorrectly implementing the project's required technologies. 

Group brainstorming and discussion ensure the identification of the greatest number of technical issues. A diverse range of expertise and experience can help achieve this, as many people join projects from different technical backgrounds, thus heightening the team's technical knowledge. Identification of technical risks also helps team members become aware of new skills they may need for the project. 

See *Table 1* for our list of technical risks.

## Project Management Risks

Project management risks arise from traditional constraints on scope, budget and time. As this is a university project, budget constraints are not applicable. However, scope and time constraint risks are still relevant.

Scope-related risks involve circumstances resulting from an inadequate or incorrect definition of project scope. This makes outlining what work needs to be done difficult. The common theme in mitigation strategies for these risks primarily revolves around improving communication within the team and with the client. These factors also mean an Agile methodology works more effectively than traditional waterfall methods. 

See *Table 2* for our list of scope-related risks.

Time risks (the meaning of which speaks for itself) results in the team’s technical expertise being unapplied to do-able tasks in the project. This can result in some project requirements being left uncompleted. Assuming an appropriate scope for the project \- as time requirements are linked to the size of the project \- many time risks develop as a result of ignorance and / or because of poor project management. In this context, ignorance refers to the team not knowing what it doesn’t know. The learning curve associated with any new project may see readjustments to estimates of time investments for tasks. To prevent this from impacting delivery, conservative estimates of our own ability and knowledge are made when delegating tasks to team members. General poor project management pertaining to time risks can be mitigated by good communication, effective delegation of tasks and thorough planning. In software development, and for this project, these ideas are applied within an agile framework. 

See *Table 3* for our list of time-related risks.

## Conclusion and Summary

This register discusses two major categories of risks \- technical and project management. Identification of technical risks helps define requirements and ensures the team understands what is required of them to deliver appropriate software for the project. It is critical to the planning phase of the project and helps ensure the project's systems work correctly. The project management risks illustrate how traditional time and scope constraints can negatively impact a project's development. Identification of these risks and potential mitigation strategies assist the team in correctly applying an agile style of project management. This will help to ensure a successful delivery of the project. 

### Table 1: Technical Risks

| Description of Risk | Negative Outcome  | Mitigation Plan  |
| :---- | :---- | :---- |
| Our software and code meets client requirements but is unintuitive and challenging to use in the field. | Reduced functionality and usability. | Consider implementing or planning what the project's MVP (Minimum Value Product) might look like.  Frequently consult with clients (per Agile and Scrum methodologies). Provide clients with mock-up GUIs and detailed descriptions of potential user experience. Develop and rely on user stories to understand how the client interacts with the project. Develop suitable documentation |
| Inadequate acceptance tests.  | Assessing the team’s performance quality at the end of sprints 2 and 3 may be impaired if pre-defined tests don’t cover what we developed in those sprints.  | Discuss tests in group meetings to transform diverse ideas into the acceptance tests. |
| Incorrect output of colour data and graphs due to incorrect backend implementation.  | The output of the project is incorrect, rendering the project unusable.  | Prior to project delivery, test our system using photos and colour values from similar studies.  |
| The system doesn’t identify and communicate to the user when false values may occur in output (e.g. photos are too low quality, photos are cropping out parts of the core) | If the user's input (sediment core photo) is inadequate and they are not informed, they may be unaware of output inaccuracies. | Encourage the users and client to take high-quality input photos. Ensure we develop a system to show users relevant error messages. |
| Documentation meets requirements but is inaccessible and difficult for inexperienced tech users to understand.  | Users who last used the project a while ago may struggle to use it or to re-learn the system.  | Write highly granular, specific documentation with clear, concise and easy-to-understand instructions.  Develop the documentation in liaison with the client to gauge the effectiveness of the documentation's instructions. |
| The space complexity of high-resolution image processing hampers the system’s performance.  | The program's usability may be reduced if inputs take too long to process. | Discuss the ideal hardware specifications with the client.  Write efficient code (e.g. use linear algebra instead of iterating over arrays) |
| Selecting non-image files as input breaks system components. | Could break or cause issues when later using the application. | Implement a system that checks and screens all inputted files.  |

### 

### Table 2: Project Management Risks \- Scope 

| Description of Risk | Negative Outcome  | Mitigation Plan  |
| :---- | :---- | :---- |
| Misunderstanding project requirements.   | The software developed for the client doesn’t meet their needs. Functionality and usefulness are reduced.  | Conduct and review the $100 test on project requirements.  Attempt to understand why the client valued the project's requirements. |
| Client-side project requirements change.  | Some software and code may be made redundant, resulting in wasted effort and time. | Frequent consultation with clients (following Agile and Scrum methodologies). |
| The application of the project and its software conflicts with the wishes and expectations expressed by cultural heritage-related stakeholders. | The geological cores being analysed are sourced from a culturally significant Indigenous site.  Potential positives from the project and its later research could be negated if our methodologies conflict with the wishes of Indigenous stakeholders.  | Stay up to date with communication from the client about these potential issues.  The client has communicated to the team that permission has been granted.				 |
| Intellectual property issues arise during the development or later application of the project.  | Incorrect licensing may make the project application in the field more difficult if licensing is reported on incorrectly.  | Follow universities and the client’s guidelines for licensing requirements. Communicate with clients on any further issues that arise during project development. 	 |
| Unfortunate but necessary cuts to scope aren’t made when required.  | Reduced functionality and quality of delivered project.  | Keep up to date with progress to reduce the chance that the team unexpectedly doesn’t meet its goals. Ensure the team is being as realistic as possible when delegating tasks and assessing what is possible. |

### Table 3: Project Management Risks \- Time

| Description of Risk | Negative Outcome  | Mitigation Plan  |
| :---- | :---- | :---- |
| Time constraints risk the completion of project deliverables. | Critical elements of the project requirements may be missing when delivered to the client.  | Clearly define the project's scope in the first sprint. Agree upon a realistic scope with the client. Develop a hierarchy of requirements so that critical requirements are completed first ($100 Test). Assign roles and tasks to team members to improve efficiency and maintain accountability.  Adjust the scope where necessary per agile and scrum principles. Efficiently communicate these changes to the client. |
| Time pressure due to the development learning curve increases the difficulty of meeting the project requirements.  | Completing project deliverables may become more difficult and take more time.  | Discuss preferences for development frameworks in group meetings so that the most suitable framework is chosen.  Decide which framework to use in the planning stage so that developers can learn the required new skills before coding/development begins. 				 |
| The team consistently underestimates the time required to complete tasks. | Critical elements of the project requirements may be missing when delivered to the client.  | Follow our mentor’s advice and double original estimates for time required to complete tasks. Plan flexibly so that additional time can be given to tasks that are taking longer than expected.  |

