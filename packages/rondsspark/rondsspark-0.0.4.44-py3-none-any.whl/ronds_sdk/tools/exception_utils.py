from ronds_sdk.models.graph import ExceptionExe


class ExceptionUtils(object):
    @staticmethod
    def get_exception(exception: str,
                      exceptiontype: str,
                      issuer: str,
                      time: str,
                      group: str,
                      inputjson: str,
                      runningtime: str) -> ExceptionExe:
        return {'exception': exception,
                'exceptiontype': exceptiontype,
                'issuer': issuer,
                'time': time,
                'group': group,
                'inputjson': inputjson,
                'runningtime': runningtime}
