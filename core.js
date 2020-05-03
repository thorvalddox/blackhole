// Transcrypt'ed from Python, 2020-05-03 16:36:51
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {shuffle} from './random.js';
var __name__ = '__main__';
export var tokens = [1, -(1), 2, -(2), 3, -(3), 4, -(4), 5, -(5), 6, -(6), 7, -(7), 8, -(8), 9, -(9), 10, -(10)];
export var tiles = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 20, 21, 22, 23, 30, 31, 32, 40, 41, 50];
export var neighbors = function* (tile) {
	for (var x of [tile - 10, tile - 9, tile - 1, tile + 1, tile + 9, tile + 10]) {
		if (__in__ (x, tiles)) {
			yield x;
		}
	}
	};
export var Board =  __class__ ('Board', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, moves) {
		self.moves = list (moves);
		self.avtiles = set (tiles).difference (set (self.moves));
	});},
	get get_value () {return __get__ (this, function (self, tile) {
		if (!__in__ (tile, self.moves)) {
			return 0;
		}
		else {
			return tokens [self.moves.index (tile)];
		}
	});},
	get get_next () {return __get__ (this, function (self, x) {
		var moves = self.moves.__getslice__ (0, null, 1);
		moves.append (x);
		return Board (moves);
	});},
	get get_pos_next () {return __get__ (this, function* (self) {
		for (var x of self.avtiles) {
			yield self.get_next (x);
		}
		});},
	get is_finished () {return __get__ (this, function (self) {
		return len (self.avtiles) == 1;
	});},
	get get_random_finish () {return __get__ (this, function (self, firstmove) {
		var b = self.get_next (firstmove);
		var R = list (b.avtiles);
		shuffle (R);
		var R = R [-(1)];
		var R2 = b.moves.__getslice__ (0, null, 1);
		R2.extend (R);
		print (R2);
		return Board (R2);
	});},
	get get_score () {return __get__ (this, function (self) {
		var s = 0;
		for (var x of neighbors (list (self.avtiles) [0])) {
			s += self.get_value (x);
		}
		return s;
	});},
	get get_move_mcts () {return __get__ (this, function (self, x, rep) {
		var s = 0;
		for (var i = 0; i < rep; i++) {
			s += self.get_random_finish (x).get_score ();
		}
		return float (s) / rep;
	});},
	get best_move () {return __get__ (this, function (self, rep) {
		var smax = 0;
		var bm = null;
		for (var x of self.avtiles) {
			var s = self.get_move_mcts (x, rep);
			print (s);
			if (bm === null || smax < s) {
				var s = smax;
				var bm = x;
			}
		}
		return bm;
	});}
});
export var Tile =  __class__ ('Tile', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, tile, mv) {
		self.tile = tile;
		self.move = mv;
	});},
	get get_tile () {return __get__ (this, function (self) {
		return document.getElementById ('tile_{}'.format (self.tile));
	});},
	get get_text () {return __get__ (this, function (self) {
		return document.getElementById ('text_{}'.format (self.tile));
	});},
	get register () {return __get__ (this, function (self, parent) {
		self.parent = parent;
		self.get_tile ().addEventListener ('click', self.fire);
	});},
	get unregister () {return __get__ (this, function (self) {
		self.get_tile ().removeEventListener ('click', self.fire);
	});},
	get fire () {return __get__ (this, function (self) {
		print ('move', self.tile);
		self.parent.player_move (self);
	});}
});
export var Interact =  __class__ ('Interact', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		self.cb = Board ([]);
		self.tiles = dict ({});
		self.rf = 0;
		self.lock = false;
	});},
	get perform_move () {return __get__ (this, function (self, tile) {
		if (len (self.cb.avtiles) <= 1) {
			return ;
		}
		var token = tokens [len (self.cb.moves)];
		if (token > 0) {
			tile.get_tile ().style.fill = 'orange';
		}
		else {
			tile.get_tile ().style.fill = 'cyan';
		}
		tile.get_text ().innerHTML = str (abs (token));
		tile.get_tile ().style.display = 'none';
		tile.get_tile ().style.display = 'block';
		self.cb = self.cb.get_next (tile.tile);
	});},
	get reflow () {return __get__ (this, function (self) {
		self.rf = document.getElementById ('blackholeroot').offsetHeight;
	});},
	get player_move () {return __get__ (this, function (self, tile) {
		print (tile.tile);
		print (tile.move);
		if (!(__in__ (tile.tile, self.cb.avtiles))) {
			return ;
		}
		if (tile.move != len (self.cb.moves)) {
			return ;
		}
		if (self.lock) {
			return ;
		}
		self.lock = true;
		self.perform_move (tile);
		self.perform_move (self.ai_tile ());
		self.lock = false;
		self.register ();
	});},
	get ai_tile () {return __get__ (this, function (self) {
		var m = self.cb.best_move (1000);
		return self.tiles [m];
	});},
	get register () {return __get__ (this, function (self) {
		for (var tile of tiles) {
			var t = Tile (tile, len (self.cb.moves));
			t.register (self);
			self.tiles [tile] = t;
		}
	});},
	get unregister () {return __get__ (this, function (self) {
		for (var [k, v] of self.tiles.py_items ()) {
			print (k, v.tile);
			v.unregister ();
		}
	});}
});
Interact ().register ();

//# sourceMappingURL=core.map