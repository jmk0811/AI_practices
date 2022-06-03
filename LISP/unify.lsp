;; Sample input:
;; (setf i1 '((P (var x) c) (Q (var x))))         ; same as forall(x) P(x,c) OR Q(x) in CNF
;; (setf i2 '((P (var y) (var z)) (Q d)))         ; same as forall(y,z) P(y,z) OR Q(d) in CNF
;; (unify i1 i2 '())                              ; this should result in the following result:
;; (((VAR Y) . D) ((VAR Z) . C) ((VAR X) VAR Y))  ; same as y/d, z/c, x/y. 
;;                                                ; another acceptable answer: y/d, z/c, x/d
;; (setf i3 '((P c a) (Q c)))                     ; same as P(c,a) OR Q(c)
;; (unify i1 i3 '())                              ; FAILED
(defun unify (p1 p2) (unify-helper p1 p2 '()))

(defun unify-helper (p1 p2 sub-list)
    (cond ((equal sub-list 'failed) 'failed)
          ((varp p1) (match-var p1 p2 sub-list))
          ((varp p2) (match-var p2 p1 sub-list))
          ((is-constant-p p1)
            (cond ((equal p1 p2) sub-list)
                  (t 'failed)))
          ((is-constant-p p2) 'failed)
          (t (unify-helper (cdr p1) (cdr p2) (unify-helper (car p1) (car p2) sub-list)))))

;; if constant return t else nil
(defun is-constant-p (p) (atom p))

; if variable return t else nil
(defun varp (p1)
      (and (listp p1) (equal (car p1) 'var)))

; helper function of match-var: makes the substitution in the sub-list
(defun substitute (p1 sub-list)
      (cond ((equal sub-list nil) p1)
            ((equal p1 (car (car sub-list))) (cdr (car sub-list)))
            (t (substitute p1 (cdr sub-list)))))

; match(unify) variables
(defun match-var (p1 p2 sub-list)
      (setf p1 (substitute p1 sub-list))
      (cond ((equal p1 p2) 'failed)
            (t (cons (cons p1 p2) sub-list))))

(setf i1 '((P (var x) c) (Q (var x))))
(setf i2 '((P (var y) (var z)) (Q d)))
(setf i3 '((P c a) (Q c)))

(print (unify i1 i2))





