import token
next
class Direction():
    Previous = 'previous'
    Next = 'next'

def construct_page_token(page_id, direction):
    return token.encrypt_string("%s+%s" % (page_id, direction))

def deconstruct_page_token(page_token):
    return token.decrypt_string(page_token).split('+')
