;;; cipher.el --- Simple string cipher for Emacs

;;; Commentary:

;; This is only-way cipher tool

;;; Code:

(defun fletcher (a b s)
  (if (string= "" s)
      (logior a (ash b 8))
    (let* ((a_ (mod (+ a (seq-first s)) 255))
           (b_ (mod (+ b a_) 255)))
      (fletcher a_ b_ (seq-rest s)))))

(defun some-number (n)
  "This function thansforms N into another number."
  (let* ((m (expt 2 32))
         (n0 (mod n m))
         (n1 (mod (logxor n0 (ash n0 13)) m))
         (n2 (mod (logxor n1 (ash n1 -17)) m))
         (n3 (mod (logxor n2 (ash n2 5)) m))
         )
    n3)
  )

(defun cipher-string (s)
  "Make some magic with S."
  (car (seq-reduce
        (lambda (p c)
          (let* ((rest (car p))
                 (n0 (cdr p))
                 (n1 (some-number n0)))
            (cons
             (concat rest
                     (format "%02x"
                      (mod (+ c n0) 256)))
             n1)
            )
          )
        s (cons "" (length s))))
  )

(defun cipher-buffer ()
  "Cipher current buffer in-place."
  (interactive)
  (let ((ciphered (cipher-string (buffer-string))))
    (erase-buffer)
    (insert ciphered)
    (save-buffer)
    )
  )

(provide 'cipher)
;;; cipher.el ends here
