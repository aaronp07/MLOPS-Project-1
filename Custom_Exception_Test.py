from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def DividedByTwoValue(a, b):
    try:
        result = a/b
        logger.info('Dividing two number')
        return result
    except Exception as e:
        logger.error('Error o(ccured')
        raise CustomException('Custom Error Zero', sys)
    
if __name__ == '__main__':
    try:
        logger.info('Starting main program')
        DividedByTwoValue(10, 10)
    except CustomException as ex:
        logger.error(str(ex))