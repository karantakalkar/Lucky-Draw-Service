# Lucky Draw App

### Running the server

Create a new virtual environment
```
python3 -m venv drf
```
Activate virtual environment
```
source drf/bin/activate
```
Install the dependencies from requirements.txt and run the command in `back-end` directory.
```
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
$ python3 manage.py runserver
```

### Setting up front-end interface

Install angular cli globally.
```
npm install -g @angular/cli
```

`cd` into `front-end` directory and install the dependencies.

```
npm install
```
Set `apiUrl` in `environment.ts` to the port where server is running, default api url is `http://localhost:8080`.

To preview the app, run the following command and navigate to `http://localhost:4200/`.
```
ng serve
```
### Architecture

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![arch](https://user-images.githubusercontent.com/54709463/143023164-07c4b5cb-2058-4e79-bda1-b0a4213f83b9.jpg)

### Getting started: Create an account

| Landing |
| --- |
| ![Screenshot from 2021-11-23 15-36-21](https://user-images.githubusercontent.com/54709463/143007693-6673b67d-eafa-4441-8192-02d2c2f3f49d.png) |

A user id will be required to acquire tickets which can be then used to participate in luck draws and win rewards.

- `/users/`   `["POST"]`  Register a new user.<br>
Format
```json
{
    "username":"t2",
    "email":"t2@t.com",
    "password":"testing321",
    "is_staff": false
}
```
Setting the `is_staff` field to true enables staff login in front-end and allows user to compute winners of lucky draws.

- `/users/login/`   `["POST"]`  Sign in as existing user<br>
Format
```json
{
    "username":"t2",
    "password":"testing321"
}
```

### Get raffle tickets (Task 1)


| Get Tickets |
| --- |
| ![Screenshot from 2021-11-23 16-20-33](https://user-images.githubusercontent.com/54709463/143011404-95f98de0-7553-4687-93aa-f03e41ad2747.png) |

User can buy a single ticket or multiple tickets in one request.

- `/tickets/`   `["POST"]` 
- `/tickets/?amount={{x}}`   `["POST"]`  <br>
Format
```json
{
    "user":"3"
}
```

### Upcoming Lucky Draw Event(s) (Task 2)

| All | Immediate |
| --- | --- |
| ![Screenshot from 2021-11-23 18-01-32](https://user-images.githubusercontent.com/54709463/143024492-bc802976-f578-4f5f-b982-8c72543323ba.png) | ![Screenshot from 2021-11-23 18-01-44](https://user-images.githubusercontent.com/54709463/143024574-7e137df6-ff00-4e2f-a9ae-e93cd8f39cf6.png)  | 

- `/luckydraws/{{pk}}`   `["GET"]`  `rewards` attribute of a lucky draw contains all upcoming rewards and their announce date. <br>

- `/luckydraws/{{pk}}/nextevent`   `["GET"]` Immediate upcoming active event for a lucky draw <br>

### Register for a lucky draw (Task 3)

| Participate | Tickets |
| --- | --- |
| ![Screenshot from 2021-11-23 16-53-57](https://user-images.githubusercontent.com/54709463/143015961-50274eed-01fd-4e1d-9b9b-74445d0370fa.png) | ![Screenshot from 2021-11-23 16-20-57](https://user-images.githubusercontent.com/54709463/143015967-a22e8ac0-2f5b-45c1-9f88-c2d87f7b1434.png) |

- `/luckydraws/{{pk}}/register/`   `["POST"]`  Register in a lucky draw using raffle ticket.<br>
Format
```json
{
    "ticket_id":"4"
}
```

### List all events in last one week (Task 4)

| List Winners |
| --- |
|  ![Screenshot from 2021-11-23 17-38-53](https://user-images.githubusercontent.com/54709463/143021659-72dd1c3a-caf3-4f62-a3ae-e74b9b32538b.png) |

Get all winners or specify `span` query parameter ( = 7) to get all winners in specified duration.

- `/winners` `["GET"]`
- `/winners/span={{x}}`   `["GET"]`  <br>

### Compute winners of lucky draw (Task 5)

| Compute Winners |
| --- |
|  ![Screenshot from 2021-11-23 17-02-39](https://user-images.githubusercontent.com/54709463/143017010-4ae99c22-e98b-4bef-88bb-7472b6423f63.png) |


- `/luckydraws/{{pk}}/compute/`   `["POST"]`  Announce the winner of a lucky draw event<br>
Format
```json
{
    "redeem_date": "2021-11-23"
}
```
### Further enhancements possible

1) Securing admin endpoints using authentication and permissions in back-end and corresponding routes using auth guard in front-end.
2) Enhancing application logic and interface based on PRD details.
3) Unit tests for both front-end and back-end
