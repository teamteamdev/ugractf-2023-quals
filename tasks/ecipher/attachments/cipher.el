;;; cipher.el --- Simple string cipher for Emacs
;;; Code:

(defun fletcher (a b s) (if (string= "" s) (logior a (ash b 8)) (let* ((a_ (mod (+ a (seq-first s)) 255)) (b_ (mod (+ b a_) 255))) (fletcher a_ b_ (seq-rest s)))))

(defun some-number (ki) (let* ((ti (expt 2 32)) (ab (mod ki ti)) (ba (mod (logxor ab (ash ab 13)) ti)) (aa (mod (logxor ba (ash ba -17)) ti)) (bb (mod (logxor aa (ash aa 5)) ti))) bb))

(defun cipher-string (po) (car (seq-reduce (lambda (goo cu) (let* ((noko (fletcher 0 0 goo)) (ji (car goo)) (ki (cdr goo)) (ti (some-number ki))) (cons (concat ji (format "%02x" (mod (+ cu ki) 256))) ti))) po (cons "" (length po)))))

(defun cipher-buffer () (interactive) (let ((ki (cipher-string (buffer-string)))) (erase-buffer) (insert ki) (save-buffer)))

(provide 'cipher)
;;; cipher.el ends here
