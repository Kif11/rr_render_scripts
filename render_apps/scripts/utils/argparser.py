import re
from logger import Logger

class ArgumentParser(object):


    def __init__(self, app_name, args_string):

        self._APP_ARG_FILE = 'app_arg.json'

        self._MAYA = 'RRMaya'
        self._3DSMAX = 'RR3dsmax'

        self.log = Logger(debug=True)

        self.app_name = app_name
        self.args_string = args_string

        self._args_dict = self._get_args()

    def _normalize(self, value):
        # Removing trailing and lead whitespaces
        value = value.rstrip()
        value = value.lstrip()

        if (len(value) == 0):
            return None

        # Convert arg calue to python type
        constructors = [int, float, str]
        for c in constructors:
            try:
                value = c(value)
                break
            except ValueError:
                pass

        # Conver string to bool
        bool_dict = {'true': True, 'false': False}
        if value in bool_dict.keys():
            value = bool_dict[value]

        return value

    def _get_args(self):
        """
        :returns: Arguments dictionary for specific app
        """
        if self.app_name == self._MAYA:
            return self._get_maya_args()
        elif self.app_name == self._3DSMAX:
            return self._get_3dsmax_args()
        else:
            return None
            self.log.error('Unknown application "%s". '
                           'App name should match'
                           'its class name.' % self.app_name)

    def _get_maya_args(self):
        """
        This metod must always return a dict of properly
        formated key value pairs.

        :returns dict: {argument_name: argument_value}
        """
        # Split argument string to a list of tuples (arg, value)
        # e.g (arg_name: arg_value)
        pattern = re.compile(r"([A-Za-z]*):\s([A-Za-z:\\ /_0-9.<>]*)")
        search = re.findall(pattern, self.args_string)

        # Pack the list of key value pair tuples to the dict
        args_dict = {i[0].rstrip(): self._normalize(i[1]) for i in search}

        # self.log.debug('Maya normalized command line argumens %s' % args_dict)

        return args_dict

    def _get_3dsmax_args(self):
        pass

    def get(self, name):
        """
        Public method to retrive argument value by name.

        :returns: Argument value. Can be string, int, float or bool
        """
        if name in self._args_dict:
            return self._args_dict[name]
        else:
            self.log.debug('Argument with name "%s" doesn not exist. '
                             'Returning None' % name)
            return None

    def set(self, name, value):
        """
        Append new argument to the list of arguments.
        :value: Has to be a particular python type such as int, str etc.
        :returns: Argument value.
        """
        self._args_dict[name] = value

        return value

    def default(self, name, value):
        """
        Create or set argument name and value.
        If argument exist but has no value this method will set it.
        :name string: Name of the argument.
        :value: Argument value.
        :returns: Will return value of the argument if exist, else return
        default value.
        """
        # Firs check if the name is in argument dict
        # if not create new key value pair
        if name not in self._args_dict:
            self.set(name, value)
            self.log.info('New argument "%s" with value '
                          '"%s" was created.' % (name, value))
            return value
        # Argument exist but no value had been set
        elif (self.get(name) is None):
            self.set(name, value)
            self.log.info('Argument "%s" set to '
                          '"%s" value.' % (name, value))
            return value
        # Argument and its value already set
        else:
            return self.get(name)


if __name__ == "__main__":

    args_string_maya = "PyModPath: C:\Program Files\Render, TestBool: true, NoneTestArg:  , Renderer: mayaSoftware, SName: /Users/amy/Desktop/RR/testProject/scenes/test_01.ma, Db: /Users/amy/Documents/maya/projects/default/,  Camera: persp, FDir:  /Users/amy/Documents/maya/projects/default/images , FNameNoVar: test_01.  , FName: maya_01  , FPadding: 4, FExt: .jpg,   FrStart: 2, FrEnd: 3, FrStep: 1 , FrOffset: 0 , Threads:  4,"
    args_string_arnold = " PyModPath: /Users/amy/rrServer/render_apps/scripts, Renderer: arnold, SName: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/scenes/arnold/rr_arnold_01.ma, Db: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/scenes/arnold/,  Camera: persp, FDir:  /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/scenes/arnold/images , FName: <RenderPass>/rr_arnold_01  , FNameNoVar: beauty/rr_arnold_01_  , FPadding: 4, FExt: .png, FExtOverride: True,  FrStart: 1, FrEnd: 10, FrStep: 9 , FrOffset: 0 , RenderDemo: False, Threads:  4,   Verbose: 0,    "

    args_maya = ArgumentParser('RRMaya', args_string_maya)
    args_arnold = ArgumentParser('RRMaya', args_string_arnold)

    print args_arnold.get('RenderMotionBlur')
