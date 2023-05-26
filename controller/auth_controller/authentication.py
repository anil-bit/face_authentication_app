from pydantic import BaseModel
from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse
from face_auth.entity.user import User
from face_auth.buisness_val.user_val import RegisterValidation

class Login(BaseModel):
    #this is base model for login
    email_id:str
    password:str

class Register(BaseModel):
    #this is the base model for register
    Name:str
    Username:str
    email_id:str
    ph_no:int
    password1:str
    password2:str


router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   responses={"401": {"description": "Not Authorized!!!"}},
                   )


@router.get("/register",response_class=JSONResponse)
async def authentication_page(request: Request):
    """
    route for user regestration
    :param request:
    :return: register response
    """
    try:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message":"registration page"})
    except Exception as e:
        raise e

@router.post("/register",response_class=JSONResponse)
async def register_user(request:Request,register:Register):
    """
    post request to register a user
    :param request:request the object
    :param register:Name: str
                    username: str
                    email_id: str
                    ph_no: int
                    password1: str
                    password2: str
    :return:Will redirect to the embedding generation route and return the UUID of user
    """
    try:
        name= register.Name
        username = register.Username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        #add uuid to the session
        user = User(name,username,email_id,ph_no,password1,password2)
        request.session["uuid"] = user.uuid_

        #after entering the registration data we have to validate wether the data format is right or wrong
        user_regestration = RegisterValidation(user)
        validate_registration = user_regestration.validate_registration()

        if not validate_registration["status"]:
            msg = validate_registration["msg"]
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response

        #save user if validation is
        validation_status = user_regestration.authenticate_user_registration()
        msg = "Registration Successful...Please Login to continue"
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )
        return response
    except Exception as e:
        raise e


