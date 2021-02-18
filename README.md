# CAPSTONE-FSND [UDACITY]

## Live URL
* https://x1999-coder.herokuapp.com

## SETTING UP

- Installing Dependencies:

```
pip install -r requirements.txt
```

- Exporting Tokens:

```
source setup.sh
```

## Authentication Permissions

- STAFF:
Can GET (coders & programs), POST, PATCH and DELETE (programs).
- USER:
Can GET (coders & programs) and POST (programs).

## Endpoints
### ["GET"] /programs
-  Returns all the programs.
-  Example Response:
```
{
  "programs": {
  {
      "id": 1,
      "title": "Code4UDACITY",
      "description": "MY NEW PROJECT",
      "coderUsername": "1999xCoder"
  },
    {
      "id": 2,
      "title": "Code4LIFE",
      "description": "MY CAPSTONE PROJECT",
      "coderUsername": "1999xCoder"
    },
  },
  "success": true
}
```

### ["GET"] /coders
-  Returns all the coders.
-  Example Response:
```
{
  "coders": {
  {
      "id": 1,
      "username": "1999xCoder"
  },
  },
  "success": true
}
```

### ["DELETE"] /programs/<<int:PID>>
-  Deletes program with given ID.
-  Example Response:
```
{
  "success": true,
  "delete": 1
}
```

### ["POST"] /programs
-  Creates a new program.
-  Example Request parameter:  ```{ "title": "Code4UDACITY", "description": "MY NEW PROJECT", "coderUsername": "1999xCoder" }```
-  Example Response:
```
{
  "program": {
  {
      "id": 1,
      "title": "Code4UDACITY",
      "description": "MY NEW PROJECT",
      "coderUsername": "1999xCoder"
  },
  },
  "success": true
}
```

### ["PATCH"] /programs/<<int:PID>>
-  Updating a program with given ID.
- Example Request parameter:  ```{ "title": "Code4UDACITY", "description": "MY CAPSTONE PROJECT" }```
-  Example Response:
```
{
  "program": {
  {
      "id": 1,
      "title": "Code4UDACITY",
      "description": "MY CAPSTONE PROJECT",
      "coderUsername": "1999xCoder"
  },
  },
  "success": true
}
```

## Error Handlers
- 401 - Unauthorized.
- 422 - Unprocessable Entity.
- Example:
```
{
  "success": "False",
  "status": 401,
  "message": "Unauthorized"
}
```
