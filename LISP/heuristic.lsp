(defvar goal-state '((1 2 3) (4 5 6) (7 8 B)))
(defvar curr-state '((1 2 8) (4 5 6) (7 3 B)))

; find the index of the given number
(defun find-index (state n)
    (dotimes (i 3)
        (dotimes (j 3)
            (let ((target (nth j (nth i state))))
                (cond ((eq n target) (return-from find-index (cons i j))))))))

; calculate the individual cost for each given number
(defun cost (n)
    (let ((gi (car (find-index goal-state n)))
          (gj (cdr (find-index goal-state n)))
          (ci (car (find-index curr-state n)))
          (cj (cdr (find-index curr-state n)))) 
    (sqrt (+ (expt (- ci gi) 2) (expt (- cj gj) 2)))))

; calculate the total cost-to-go
(defun euc-heur (curr-state goal-state)
    (let ((c 0)) 
        (dotimes (i 3)
            (dotimes (j 3)
                (setq c (+ c (cost (nth j (nth i goal-state)))))))
        (return-from euc-heur c)))


(print (euc-heur curr-state goal-state))


