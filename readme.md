terminal.py is the main file while runs an infinite loop. You can exit the terminal using exit().
terminal.py uses 'Linux' class of module 'linux_interface.py' for processing queries sent by user.
Code is appropriately commented wherever required.

module 'linux_interface.py' description:

class Node:
	attributes( path : String, parent_node : Node, children: List[Node])
	
class Linux:
	attributes( _root : Node, _current, _query : String)
	methods:
		public: 
			 getwd() : returns current directory
			 set_query(query : String) : sends query from terminal to linux_interface
		private:
			_cd(args : List[string]) : change directory (abs or rel path)
			_rm(args : List[string]) : remove dir (abs or rel path)
			_mkdir(args : List[string]) : create dir (abs or rel path)
			_ls(args : List[string]) : show all child dir (rel to current dir)
			_pwd(args : List[string]) : prints current dir
			_session(args : List[string]) : clears a session
			_throw_error(error : String) : wrapper fn to throw error
			_throw_success(success : String) : wrapper fn to throw success
			_is_absolute_path(given_path : String, root_path : String) : finds if path is absolute or relative
			_abs_to_rel_path(given_path : String, root_path : String) : converts from abs to rel path (rel wrt to root), if already relative no change is made
			_relative_path(string : String) : if path is absolute, converts it to rel wrt root dir. (input is guaranteed to be absolute path)