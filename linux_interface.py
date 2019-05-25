class Node:
    """
    Each folder is represented by a node. Path contains absolute path of folder and children contains list of child nodes of folder.
    parent_node tags the parent node with child for backward accessibility.
    """
    def __init__(self, path):
        self.path = path
        self.parent_node = None
        self.children = []

"""
We basically create a multi child tree and traverse those nodes for our various operations in class Linux.
"""
class Linux:
    """
    valid_commands is a class attribute. Key represents 'valid commands' and value represents number of total params passed in that command
    """
    valid_commands = {'ls':1,'pwd':1,'cd':2,'mkdir':2,'rm':2, 'session':2}

    """
    Constructor for this class. Creates a root and sets current node to be the root.
    """
    def __init__(self):
        self._root = Node('/root')
        self._root.parent_node = self._root # Root directory parent is root itself.
        self._query = None # Received query from user is stored here.
        self._current = self._root # Current node is root itself.

    """
    Receive a query from user and send it for further processing.
    """
    def set_query(self, query):
        self._query = query 
        self._query_process()
        return

    """
    Breaks down a query into an array and figures out if it is a valid query
    """
    def _query_process(self):
        # Breaking down a query for further processing
        query_breakdown = self._query.strip().split(' ')
        command = query_breakdown[0] # First param will be a command
        if command == '': # Blank entry by user accounts for no action
            pass 
        elif command not in self.valid_commands:
            self._throw_error('CANNOT RECOGNIZE INPUT.')
        else:
            # Checking if command has required number of additional params along with it
            # 0 for the case where we have variable number of params
            if self.valid_commands[command] == len(query_breakdown) or self.valid_commands[command] == 0:
                method_to_call = getattr(self, '_' + query_breakdown[0])
                method_to_call(query_breakdown[1:]) #R Rest of the query passed as args to required method
            else:
                self._throw_error('INVALID USE OF COMMAND')
        return

    """
    Private Method to change directory.
    """
    def _cd(self, args):
        #Looking for '..' That would imply move back by 1 directory:
        if args[0].strip('/') == '..':
            self._current = self._current.parent_node
            self._throw_success('REACHED')
            return

        #Corner Case: if cd to root is to be done
        if args[0] == '/' :#or args[0].rstrip('/') == self._root.path:
            self._current = self._root
            self._throw_success('REACHED')
            return
        
        #Absolute path or relative path
        is_absolute_path = self._is_absolute_path(args[0], self._root.path)
        #Converts absolute path to relative path. If absolute path we start searching from root directory, if relative, we search from current dir
        path = self._relative_path(args[0])
        depth = len(path.strip('/').split('/')) #Number of potential subdirectories to traverse 
        depth_path = path.split('/') #An array that tells us which folder to lookup for at a given depth
        if is_absolute_path: # Search begins from root folder if we have absolute path
            temp_node = self._root
            dir_to_redirect = self._root.path
        else:
            temp_node = self._current # Search begins from current folder if we have relative path
            dir_to_redirect = self._current.path
        matched_depths = 0

        for i in range(depth):
            if matched_depths != i: # If prevous folder in depth_path not found implies we do not have such a path
                self._throw_error('INVALID PATH')
                return
            dir_to_redirect = dir_to_redirect + '/' + depth_path[i] # if folder at depth i is found, we will try to find folder at depth i+1
            dir_to_redirect = dir_to_redirect.rstrip('/') # This is for corner cases
            for child in temp_node.children:
                if child.path == dir_to_redirect:
                    temp_node = child
                    matched_depths += 1 # We found required folder at depth i

        if dir_to_redirect == temp_node.path: # If we have now found a valid user input path present in our folder tree, we cd to that folder
            #print(dir_to_redirect)
            self._current = temp_node
            self._throw_success('REACHED')
        else:
            self._throw_error('INVALID PATH')
        return

    """
    Required at client side to update user of current path. Useful in debigging and for user friendiness
    """
    def getcwd(self):
        return self._current.path  

    """
    Make a directory
    """
    def _mkdir(self,args):
        # Figuring if path sent is absolute or relative
        is_absolute_path = self._is_absolute_path(args[0], self._root.path)
        #Converts absolute path to relative path. If absolute path we start searching from root directory, if relative, we search from current dir
        path = self._relative_path(args[0]) 
        depth = len(path.strip('/').split('/')) #Number of potential subdirectories to traverse 
        depth_path = path.split('/') #An array that tells us which folder to lookup for at a given depth
        if is_absolute_path: # lookup begins from root folder if we have absolute path
            lookup_dir = self._root.path
            temp_node = self._root
        else: # lookup begins from current folder if we have absolute path
            lookup_dir = self._current.path 
            temp_node = self._current

        count_of_existing_subpaths = 0 # If all paths exist, dir already exists, else we have to create folders at multiple levels

        #If temp_node's path is same as required path, then dir already exists
        if temp_node.path == (lookup_dir + '/' + path).rstrip('/'):
            self._throw_error('DIRECTORY ALREADY EXISTS')
            return

        for i in range(depth):
            # Have we found already existing dir at depth i?. If yes we move to that dir and continue search, else create new node
            found_at_depth_i = 0 
            lookup_dir = lookup_dir + '/' + depth_path[i]
            lookup_dir = lookup_dir.rstrip('/')
            #Find if this is present, if present change temp_node to that child and proceed, else create a new child
            for child in temp_node.children:
                if child.path == lookup_dir:
                    count_of_existing_subpaths += 1
                    found_at_depth_i = 1
                    temp_node = child
            if found_at_depth_i == 0:
                new_node = Node(lookup_dir)
                new_node.parent_node = temp_node
                temp_node.children.append(new_node) # Add a new child to that node and then move to that child and proceed further
                temp_node = new_node
        if count_of_existing_subpaths == depth: # If all folders existed in a sequential order, means that dir exists already
            self._throw_error('DIRECTORY ALREADY EXISTS')
        else:
            self._throw_success('CREATED')
        return        

    """
    Removing a folder. It will remove other sub folders as well
    """
    def _rm(self, args):

        # Corner Case
        if args[0] == '/' or args[0].rstrip('/') == self._root.path:
            self._throw_error('CANNOT DELETE ROOT')
            return

        # Figurig if it is absolute path or relative path
        is_absolute_path = self._is_absolute_path(args[0], self._root.path)
        #Converts absolute path to relative path. If absolute path we start searching from root directory, if relative, we search from current dir
        path = self._relative_path(args[0])
        depth = len(path.strip('/').split('/')) #Number of potential subdirectories to traverse 
        depth_path = path.split('/') #An array that tells us which folder to lookup for at a given depth
        if is_absolute_path: # Search begins from root folder if we have absolute path
            temp_node = self._root
            dir_to_redirect = self._root.path
        else: # Search begins from current folder if we have absolute path
            temp_node = self._current
            dir_to_redirect = self._current.path
        matched_depths = 0

        for i in range(depth):
            if matched_depths != i: # If prevous folder in depth_path not found implies we do not have such a path
                self._throw_error('INVALID PATH')
                return
            dir_to_redirect = dir_to_redirect + '/' + depth_path[i] # if folder at depth i is found, we will try to find folder at depth i+1
            dir_to_redirect = dir_to_redirect.rstrip('/') # This is for corner cases
            for child in temp_node.children:
                if child.path == dir_to_redirect:
                    temp_node = child
                    matched_depths += 1 # We found required folder at depth i

        # If we have found such a folder, then we need to erase that node from its parent and shift to last existing directory
        if dir_to_redirect == temp_node.path: 
            parent_node = temp_node.parent_node
            pop_index = parent_node.children.index(temp_node) # Position of that node in its parent's children array
            parent_node.children.pop(pop_index)
            self._throw_success('DELETED')
            if dir_to_redirect in self._current.path: 
                #need to change to parent of that dir
                self._cd([parent_node.path])
        else:
            self._throw_error('INVALID PATH')
        return                

    """
    print the current working directory
    """
    def _pwd(self, args):
        if self._current.path == self._root.path:
            print('    PATH: /')
        else:
            print('    PATH: {}'.format(self._current.path[len(self._root.path):]))
        return

    """
    list down all the paths in current directory
    """
    def _ls(self, args):
        len_curr_path = len(self._current.path)
        print('    DIRS:', end = ' ')
        for child in self._current.children:
            print(child.path[len_curr_path+1:], end = ' ') # We have to print relative path, so doing slicing
        print(' ')
        return

    """
    Performing operating dealing with session. We have session clear as our usecase
    """
    def _session(self,args):
        if args[0] == 'clear':
            self._current = self._root # curr dir set to root dir
            self._current.children = [] # all children of root cleared
            self._throw_success('CLEARED: RESET TO ROOT')
        else:
            self._throw_error('INVALID COMMAND')
        return

    """
    Creates relative path out of given path. If input is relative path, nothing is done, else relative path wrt to root folder is given
    """
    def _relative_path(self, string):
        is_absolute_path = self._is_absolute_path(string.rstrip('/'), self._root.path) #Bool method called
        if(is_absolute_path):
            path = self._abs_to_rel_path(string.rstrip(''), self._root.path) #Convert to rel path
        else:
            path = string.strip('/') # this is relative path 
        return path

    """
    Bool method which checks for absolute/ realtive path
    """
    def _is_absolute_path(self, given_path, root_path):
        if root_path in given_path:
            if given_path.index(root_path) == 0 and given_path.strip('/').split('/')[0] == root_path.strip('/'):
                return True
        return False

    """
    Converts abs to rel path
    """
    def _abs_to_rel_path(self, given_path, root_path):
        #If given path is root path then we return an empty list
        return given_path[len(root_path)+1:]

    """
    Wrapper function to print error
    """
    def _throw_error(self, error):
        print('    ERR: {}'.format(error))
        return

    """
    Wrapper function to print success
    """
    def _throw_success(self, success):
        print('    SUCC: {}'.format(success))
        return
