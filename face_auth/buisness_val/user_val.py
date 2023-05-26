import re
from face_auth.entity.user import User
from face_auth.data_access.user_data import UserData
from face_auth.logger import logging
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class LoginValidation:
    def __init__(self,email_id:str):
        self.email_id = email_id
        self.regex=re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )


    def is_email_validate(self) -> bool:
        if re.fullmatch(self.regex,self.email_id):
            return True
        else:
            return False

    def is_password_valid(self) -> bool:









class RegisterValidation:
    """
    This class authintactes the user and returns the status
    """
    def __init__(self,user:User):
        self.user = user
        self.regex = re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            )
        self.uuid = self.user.uuid_
        self.userdata = UserData()


    def validation(self):
        """
        this check all the validation condition for the registration
        :return: string
        """
        try:
            msg =""
            if self.user.Name == None:
                msg += "name is required"
            if self.user.username == None:
                msg += "username is required"
            if self.user.email_id == None:
                msg += "email id is required"
            if self.user.ph_no == None:
                msg += "phone number is required"
            if self.user.password1 == None:
                msg += "password is required"
            if self.user.password2 == None:
                msg += "confirm password is required"
            if not self.is_email_valid():
                msg += "Email is not valid"
            if not self.is_password_valid():
                msg += "Length of the pass`word should be between 8 and 16"
            if not self.is_password_match():
                msg += "password does not match"
            if not self.is_details_exsists():
                msg += "user already exsists"

            return msg
        except Exception as e:
            raise e



    def is_email_valid(self) -> bool:
        """
        this validates the email id while registration
        :return:if email id is valid it return true or else it return false
        """

        if re.fullmatch(self.regex, self.user.email_id):
            return True
        else:
            return False

    def is_password_valid(self)->bool:
        """
        thsi validates the password
        :return:
        """
        if len(self.user.password1)>=8 and len(self.user.password2)<=16:
            return True
        else:
            return False


    def is_password_match(self)->bool:
        """
        thsi checks wether the password1 and password2 match or not
        :return: TRue or false
        """
        if self.user.password1==self.user.password2:
            return True
        else:
            return False

    def is_details_exsists(self)->bool:
        username_val = self.userdata.get_user({"username": self.user.username})
        emailid_val = self.userdata.get_user({"email_id":self.user.email_id})
        uuid_val = self.userdata.get_user({"UUID":self.uuid})
        if username_val==None and emailid_val==None and uuid_val == None:
            return True
        else:
            return False

    @staticmethod
    def get_password_hash(password:str)->str:
        return bcrypt_context.hash(password)

    def validate_registration(self)->bool:
        """
        this you can check validation conditions for user registration
        :param self:
        :return:
        """
        if len(self.validation)!=0:
            return {"status": False, "msg": self.validate()}
        else:
            return {"status":True}


    def authenticate_user_registration(self)->bool:
        """
        this saves the user details in database after validation of user is done

        :return:
        """
        try:
            logging.info("validating the user details while registration.......")
            if self.validate_registration()["status"]:
                logging.info("genrating the password hash.....")
                hashed_password: str = self.get_password_hash(self.user.password1)
                user_data_dict: dict = {
                    "Name":self.user.Name,
                    "username":self.user.username,
                    "password":hashed_password,
                    "ph_no":self.user.ph_no,
                    "UUID":self.uuid,
                }
                logging.info("saving the user details in the database")
                self.userdata.save_user(user_data_dict)
                logging .info("saving the user details completed")
                return {"status":True,"msg":"user registered successfully"}
            logging.info("Validation failed while Registration.....")
            return {"status": False, "msg": self.validation()}

        except Exception as e:
            raise e





        




