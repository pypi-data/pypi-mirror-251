from arsein.Error import AuthError,ErrorMethod

def ErrorRubika(ERROR):
	if ERROR['status_det'] == 'INVALID_AUTH':
		raise AuthError('your Auth is invalid')
	elif ERROR['status_det'] == 'NOT_REGISTERED':
		raise AuthError("Your account doesn't have such Auth")
	elif ERROR['status_det'] == 'INVALID_INPUT':
		raise ErrorMethod("ًInput value in the method is incorrect")
