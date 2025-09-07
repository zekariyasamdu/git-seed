from marshmallow import Schema, fields

class IpSchema(Schema):
    id = fields.Int(required=True)
    ip_address = fields.Str(required=True)   

class RepoSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class RepoWithIpSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    allowed_ips = fields.List(fields.Nested(IpSchema)) 
# Request

class CrudIpRequestSchema(Schema):
    ip_address = fields.Str(required=True)

# Response 
class ReposResponseSchema(Schema):
    repos = fields.List(fields.Nested(RepoSchema))

class ReposWithIpResponseSchema(Schema):
    repos = fields.List(fields.Nested(RepoWithIpSchema))

class IpsResponseSchema(Schema):
    ips = fields.List(fields.Nested(IpSchema))

class CrudIpResponseSchema(Schema):
    message = fields.Str()
    repo_id = fields.Int(required=True)
    ip = fields.Str(required=True)

#login 

class LoginRequestSchema(Schema):
    admin_name = fields.String(required=True)
    password = fields.String(required=True)

class LoginResponse(Schema):
    access_token = fields.Str(required=True)
    token_type = fields.Str(required=True)
    user_id = fields.Str(required=True)