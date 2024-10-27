# LBPH Face Recognition API

This API provides facial recognition functionality and CRUD operations to manage voters. It uses the Local Binary Patterns Histograms (LBPH) algorithm to identify voters based on facial images.

## Features

- **CRUD operations** to manage voter information.
- **Facial recognition** based on LBPH to identify voters using their photos.
- **Security**: passwords are stored in hashed format.

## Requirements

- Python 3.11
- Flask
- Other dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/RobertoRuben/lbph-face-recognition-api.git
    cd lbph-face-recognition-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    flask run
    ```

## API Endpoints

### 1. Create a Voter

- **URL**: `/votantes`
- **Method**: `POST`
- **Description**: Creates a new voter.
- **Parameters**:
  - Form-data:
    - `dni`: Voter's DNI.
    - `nombre`: Voter's first name.
    - `apellido_paterno`: Last name (father's side).
    - `apellido_materno`: Last name (mother's side).
    - `fecha_nacimiento`: Date of birth (YYYY-MM-DD).
    - `email`: Voter's email.
    - `password`: Voter's password.
    - `foto`: Voter's photo.
- **Sample Response**:

    ```json
    {
        "dni": "12345678",
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "fecha_nacimiento": "1990-01-01",
        "email": "juan@example.com"
    }
    ```

### 2. Get All Voters

- **URL**: `/votantes`
- **Method**: `GET`
- **Description**: Retrieves a list of all voters.
- **Sample Response**:

    ```json
    [
        {
            "dni": "12345678",
            "nombre": "Juan",
            "apellido_paterno": "Perez",
            "apellido_materno": "Gomez",
            "fecha_nacimiento": "1990-01-01",
            "email": "juan@example.com"
        },
        ...
    ]
    ```

### 3. Update a Voter

- **URL**: `/votantes/<votante_id>`
- **Method**: `PUT`
- **Description**: Updates an existing voter's information.
- **Parameters**:
  - JSON Body (only fields that need to be updated):
    - `dni` (optional)
    - `nombre` (optional)
    - `apellido_paterno` (optional)
    - `apellido_materno` (optional)
    - `fecha_nacimiento` (optional)
    - `email` (optional)
    - `password` (optional)
- **Sample Response**:

    ```json
    {
        "dni": "12345678",
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gomez",
        "fecha_nacimiento": "1990-01-01",
        "email": "juan_updated@example.com"
    }
    ```

### 4. Delete a Voter

- **URL**: `/votantes/<votante_id>`
- **Method**: `DELETE`
- **Description**: Deletes an existing voter by ID.
- **Sample Response**:

    ```json
    {
        "message": "Voter successfully deleted"
    }
    ```

### 5. Facial Recognition

- **URL**: `/reconocimiento`
- **Method**: `POST`
- **Description**: Recognizes a voter based on a base64-encoded image.
- **Parameters**:
  - JSON Body:
    - `image`: Base64-encoded image string.
- **Sample Response**:

    ```json
    {
        "apellido_materno": "Cuccitini",
        "apellido_paterno": "Messi",
        "dni": 45120396,
        "email": "messi@example.com",
        "fecha_nacimiento": "1990-01-01",
        "id_usuario": 1,
        "nombre": "Lionel Andres"
    }
    ```

## Notes

- Ensure that all images are base64-encoded for the facial recognition endpoint.
- Passwords are hashed before storing to maintain security.
