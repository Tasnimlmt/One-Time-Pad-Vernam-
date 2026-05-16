import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import random
import string
from collections import Counter
import binascii

class VernamOneTimePad:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ V E R N A M - O N E · T I M E · P A D ⚡")
        self.root.geometry("1400x950")
        self.root.configure(bg='#0a0a0a')  # Pure black/dark theme
        
        # Custom colors for this theme (AMBER/ORANGE cyberpunk)
        self.bg_color = "#0a0a0a"
        self.fg_color = "#ff6600"
        self.accent_color = "#ff9900"
        self.binary_color = "#33ff33"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top banner with binary rain effect
        self.create_binary_banner(main_container)
        
        # Create notebook with custom style
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Vernam.TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('Vernam.TNotebook.Tab', background='#1a1a1a', foreground=self.fg_color,
                       padding=[15, 8], font=('Courier', 10, 'bold'))
        style.map('Vernam.TNotebook.Tab',
                 background=[('selected', self.fg_color), ('active', '#2a2a2a')],
                 foreground=[('selected', '#0a0a0a'), ('active', self.fg_color)])
        
        notebook = ttk.Notebook(main_container, style='Vernam.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab1 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab1, text="⚡ OTP ENCRYPT/DECRYPT")
        self.setup_otp_operations()
        
        self.tab2 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab2, text="🔓 KEY REUSE ATTACK")
        self.setup_key_reuse_attack()
        
        self.tab3 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab3, text="📊 CRIB DRAGGING ATTACK")
        self.setup_crib_dragging()
        
        self.tab4 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab4, text="🛡️ PRACTICAL LIMITATIONS")
        self.setup_practical_limitations()
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_binary_banner(self, parent):
        banner = tk.Frame(parent, bg=self.bg_color, height=80)
        banner.pack(fill=tk.X, pady=(10, 0))
        
        banner_text = """
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║   ██╗   ██╗███████╗██████╗ ███╗   ██╗ █████╗ ███╗   ███╗    ██████╗ ████████╗██████╗     ║
║   ██║   ██║██╔════╝██╔══██╗████╗  ██║██╔══██╗████╗ ████║    ██╔══██╗╚══██╔══╝██╔══██╗    ║
║   ██║   ██║█████╗  ██████╔╝██╔██╗ ██║███████║██╔████╔██║    ██████╔╝   ██║   ██████╔╝    ║
║   ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║╚██╗██║██╔══██║██║╚██╔╝██║    ██╔═══╝    ██║   ██╔══██╗    ║
║    ╚████╔╝ ███████╗██║  ██║██║ ╚████║██║  ██║██║ ╚═╝ ██║    ██║        ██║   ██║  ██║    ║
║     ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝        ╚═╝   ╚═╝     ║
║                         ONE-TIME PAD - V E R N A M   C I P H E R                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
        """
        
        lbl = tk.Label(banner, text=banner_text, font=('Courier', 7), fg=self.fg_color,
                      bg=self.bg_color, justify=tk.LEFT)
        lbl.pack()
    
    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg='#1a1a1a', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="🟢 SYSTEM READY | PERFECT SECURITY MODE",
                                     font=('Courier', 9), fg=self.fg_color, bg='#1a1a1a')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Binary animation dots
        for i in range(4):
            dot = tk.Label(status_frame, text="⚡", font=('Courier', 10), fg=self.accent_color, bg='#1a1a1a')
            dot.pack(side=tk.RIGHT, padx=5)
    
    # ==================== CORE OTP FUNCTIONS ====================
    def string_to_binary(self, text):
        """Convert string to binary representation"""
        return ''.join(format(ord(c), '08b') for c in text)
    
    def binary_to_string(self, binary):
        """Convert binary back to string"""
        try:
            chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
            return ''.join(chr(int(c, 2)) for c in chars)
        except:
            return ""
    
    def generate_random_key(self, length):
        """Generate random key of given length (in bytes)"""
        return ''.join(chr(random.randint(0, 255)) for _ in range(length))
    
    def xor_strings(self, s1, s2):
        """XOR two strings byte by byte"""
        result = []
        for i in range(min(len(s1), len(s2))):
            result.append(chr(ord(s1[i]) ^ ord(s2[i])))
        return ''.join(result)
    
    def encrypt_otp(self, plaintext, key=None):
        """Encrypt using OTP. If key is None, generate random key"""
        if key is None:
            key = self.generate_random_key(len(plaintext))
        elif len(key) < len(plaintext):
            messagebox.showerror("Error", f"Key must be at least as long as plaintext! (Key: {len(key)} < {len(plaintext)})")
            return None, None
        
        ciphertext = self.xor_strings(plaintext, key[:len(plaintext)])
        return ciphertext, key
    
    def decrypt_otp(self, ciphertext, key):
        """Decrypt using OTP"""
        if len(key) < len(ciphertext):
            messagebox.showerror("Error", f"Key must be at least as long as ciphertext! (Key: {len(key)} < {len(ciphertext)})")
            return None
        return self.xor_strings(ciphertext, key[:len(ciphertext)])
    
    # ==================== TAB 1: OTP OPERATIONS ====================
    def setup_otp_operations(self):
        # Main frame
        main_frame = tk.Frame(self.tab1, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Input
        left_panel = tk.Frame(main_frame, bg=self.bg_color)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Plaintext input
        pt_frame = tk.LabelFrame(left_panel, text="📝 PLAINTEXT INPUT", 
                                 font=('Courier', 10, 'bold'),
                                 fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        pt_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.plaintext_input = scrolledtext.ScrolledText(pt_frame, height=6, font=('Consolas', 11),
                                                         bg='#1a1a1a', fg='#00ff00', insertbackground=self.fg_color)
        self.plaintext_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.plaintext_input.insert('1.0', "HELLO THIS IS A SECRET MESSAGE FOR ONE TIME PAD DEMONSTRATION")
        
        # Key input
        key_frame = tk.LabelFrame(left_panel, text="🔑 KEY (leave empty for random generation)", 
                                  font=('Courier', 10, 'bold'),
                                  fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        key_frame.pack(fill=tk.X, pady=10)
        
        self.key_input = scrolledtext.ScrolledText(key_frame, height=4, font=('Consolas', 11),
                                                   bg='#1a1a1a', fg='#00ff00')
        self.key_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="⚡ ENCRYPT", command=self.do_encrypt_otp,
                 font=('Courier', 11, 'bold'), bg=self.fg_color, fg='#0a0a0a',
                 activebackground='#ff8800', activeforeground='#0a0a0a',
                 relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔓 DECRYPT", command=self.do_decrypt_otp,
                 font=('Courier', 11, 'bold'), bg=self.accent_color, fg='#0a0a0a',
                 activebackground='#ff8800', activeforeground='#0a0a0a',
                 relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ CLEAR", command=self.clear_otp,
                 font=('Courier', 11, 'bold'), bg='#ff4444', fg='#0a0a0a',
                 activebackground='#cc0000', activeforeground='#0a0a0a',
                 relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Output
        right_panel = tk.Frame(main_frame, bg=self.bg_color)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Ciphertext output
        ct_frame = tk.LabelFrame(right_panel, text="📤 CIPHERTEXT", 
                                 font=('Courier', 10, 'bold'),
                                 fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        ct_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.ciphertext_output = scrolledtext.ScrolledText(ct_frame, height=6, font=('Consolas', 11),
                                                            bg='#1a1a1a', fg='#ff6600')
        self.ciphertext_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Key output
        keyout_frame = tk.LabelFrame(right_panel, text="🔑 GENERATED/ENTERED KEY", 
                                     font=('Courier', 10, 'bold'),
                                     fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        keyout_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.key_output = scrolledtext.ScrolledText(keyout_frame, height=4, font=('Consolas', 11),
                                                    bg='#1a1a1a', fg='#33ff33')
        self.key_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Decrypted output
        dec_frame = tk.LabelFrame(right_panel, text="📄 DECRYPTED (VERIFICATION)", 
                                  font=('Courier', 10, 'bold'),
                                  fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        dec_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.decrypted_output = scrolledtext.ScrolledText(dec_frame, height=4, font=('Consolas', 11),
                                                          bg='#1a1a1a', fg='#00ff00')
        self.decrypted_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def do_encrypt_otp(self):
        plaintext = self.plaintext_input.get('1.0', tk.END).strip()
        if not plaintext:
            messagebox.showerror("Error", "Please enter plaintext!")
            return
        
        key_text = self.key_input.get('1.0', tk.END).strip()
        key = key_text if key_text else None
        
        ciphertext, used_key = self.encrypt_otp(plaintext, key)
        
        if ciphertext is None:
            return
        
        # Display results
        self.ciphertext_output.delete('1.0', tk.END)
        self.ciphertext_output.insert('1.0', ciphertext)
        
        # Show key in hex for better visibility
        key_hex = ' '.join(format(ord(c), '02x') for c in used_key)
        self.key_output.delete('1.0', tk.END)
        self.key_output.insert('1.0', f"Raw Key (length {len(used_key)} chars):\n{used_key}\n\nHex Key:\n{key_hex}")
        
        # Verify decryption
        decrypted = self.decrypt_otp(ciphertext, used_key)
        self.decrypted_output.delete('1.0', tk.END)
        self.decrypted_output.insert('1.0', decrypted)
        
        if decrypted == plaintext:
            self.status_label.config(text="✅ ENCRYPTION VERIFIED | Perfect reconstruction achieved!")
        else:
            self.status_label.config(text="⚠️ Verification failed!")
    
    def do_decrypt_otp(self):
        ciphertext = self.ciphertext_output.get('1.0', tk.END).strip()
        key_text = self.key_input.get('1.0', tk.END).strip()
        
        if not ciphertext:
            messagebox.showerror("Error", "No ciphertext to decrypt!")
            return
        
        if not key_text:
            messagebox.showerror("Error", "Please enter the key for decryption!")
            return
        
        decrypted = self.decrypt_otp(ciphertext, key_text)
        
        if decrypted is None:
            return
        
        self.decrypted_output.delete('1.0', tk.END)
        self.decrypted_output.insert('1.0', decrypted)
        self.status_label.config(text="🔓 Decryption complete")
    
    def clear_otp(self):
        self.ciphertext_output.delete('1.0', tk.END)
        self.key_output.delete('1.0', tk.END)
        self.decrypted_output.delete('1.0', tk.END)
    
    # ==================== TAB 2: KEY REUSE ATTACK ====================
    def setup_key_reuse_attack(self):
        main_frame = tk.Frame(self.tab2, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Description
        desc_frame = tk.LabelFrame(main_frame, text="⚠️ KEY REUSE VULNERABILITY DEMONSTRATION", 
                                   font=('Courier', 10, 'bold'),
                                   fg='#ff0000', bg=self.bg_color, relief=tk.GROOVE, bd=2)
        desc_frame.pack(fill=tk.X, pady=10)
        
        desc_text = """CRITICAL: When the same key is used twice, an attacker can XOR the two ciphertexts to get M1 ⊕ M2.
This reveals patterns that can be used to recover the original messages!"""
        
        desc_lbl = tk.Label(desc_frame, text=desc_text, font=('Consolas', 10),
                           fg='#ffff00', bg=self.bg_color, wraplength=1200, justify=tk.LEFT)
        desc_lbl.pack(padx=10, pady=10)
        
        # Message 1
        msg1_frame = tk.LabelFrame(main_frame, text="📝 MESSAGE 1", 
                                   font=('Courier', 10, 'bold'),
                                   fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        msg1_frame.pack(fill=tk.X, pady=10)
        
        self.msg1_input = scrolledtext.ScrolledText(msg1_frame, height=3, font=('Consolas', 11),
                                                    bg='#1a1a1a', fg='#00ff00')
        self.msg1_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.msg1_input.insert('1.0', "ATTACK AT DAWN")
        
        # Message 2
        msg2_frame = tk.LabelFrame(main_frame, text="📝 MESSAGE 2", 
                                   font=('Courier', 10, 'bold'),
                                   fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        msg2_frame.pack(fill=tk.X, pady=10)
        
        self.msg2_input = scrolledtext.ScrolledText(msg2_frame, height=3, font=('Consolas', 11),
                                                    bg='#1a1a1a', fg='#00ff00')
        self.msg2_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.msg2_input.insert('1.0', "RETREAT AT NIGHT")
        
        # Attack button
        tk.Button(main_frame, text="🔓 PERFORM KEY REUSE ATTACK", command=self.key_reuse_attack,
                 font=('Courier', 11, 'bold'), bg='#ff4444', fg='#0a0a0a',
                 activebackground='#cc0000', activeforeground='#0a0a0a',
                 relief=tk.RAISED, bd=2).pack(pady=10)
        
        # Results
        results_frame = tk.LabelFrame(main_frame, text="🎯 ATTACK RESULTS (C1 XOR C2 = M1 XOR M2)", 
                                      font=('Courier', 10, 'bold'),
                                      fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.attack_results = scrolledtext.ScrolledText(results_frame, height=12, font=('Consolas', 10),
                                                        bg='#1a1a1a', fg='#ff6600')
        self.attack_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def key_reuse_attack(self):
        msg1 = self.msg1_input.get('1.0', tk.END).strip()
        msg2 = self.msg2_input.get('1.0', tk.END).strip()
        
        # Generate a random key
        max_len = max(len(msg1), len(msg2))
        key = self.generate_random_key(max_len)
        
        # Encrypt both messages with the SAME key
        c1, _ = self.encrypt_otp(msg1, key)
        c2, _ = self.encrypt_otp(msg2, key)
        
        # Calculate XOR of ciphertexts
        xored = self.xor_strings(c1, c2)
        
        # Calculate XOR of plaintexts for verification
        m1_m2_xor = self.xor_strings(msg1, msg2)
        
        self.attack_results.delete('1.0', tk.END)
        self.attack_results.insert('1.0', "╔══════════════════════════════════════════════════════════════════╗\n")
        self.attack_results.insert(tk.END, "║              KEY REUSE ATTACK - MATHEMATICAL PROOF              ║\n")
        self.attack_results.insert(tk.END, "╚══════════════════════════════════════════════════════════════════╝\n\n")
        
        self.attack_results.insert(tk.END, f"Message 1: {msg1}\n")
        self.attack_results.insert(tk.END, f"Message 2: {msg2}\n\n")
        
        self.attack_results.insert(tk.END, f"Ciphertext 1 (hex): {c1.encode('utf-8').hex()}\n")
        self.attack_results.insert(tk.END, f"Ciphertext 2 (hex): {c2.encode('utf-8').hex()}\n\n")
        
        self.attack_results.insert(tk.END, f"C1 ⊕ C2 (hex): {xored.encode('utf-8').hex()}\n")
        self.attack_results.insert(tk.END, f"M1 ⊕ M2 (hex): {m1_m2_xor.encode('utf-8').hex()}\n\n")
        
        self.attack_results.insert(tk.END, "🔴 CRITICAL OBSERVATION:\n")
        self.attack_results.insert(tk.END, "─" * 70 + "\n")
        self.attack_results.insert(tk.END, f"C1 ⊕ C2 = M1 ⊕ M2: {xored == m1_m2_xor}\n\n")
        
        self.attack_results.insert(tk.END, "💡 ATTACKER CAN NOW:\n")
        self.attack_results.insert(tk.END, "1. See where messages differ (non-zero bytes)\n")
        self.attack_results.insert(tk.END, "2. Guess words in one message to reveal the other\n")
        self.attack_results.insert(tk.END, "3. Use crib dragging to recover both messages\n\n")
        
        # Show where messages differ
        diff_positions = []
        for i in range(min(len(msg1), len(msg2))):
            if msg1[i] != msg2[i]:
                diff_positions.append(i)
        
        self.attack_results.insert(tk.END, f"📍 DIFFERENCE POSITIONS (M1 ≠ M2): {diff_positions}\n")
        
        self.status_label.config(text="⚠️ DEMONSTRATION: Key reuse completely compromises security!")
    
    # ==================== TAB 3: CRIB DRAGGING ATTACK ====================
    def setup_crib_dragging(self):
        main_frame = tk.Frame(self.tab3, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Explanation
        explain_frame = tk.LabelFrame(main_frame, text="📖 CRIB DRAGGING TECHNIQUE", 
                                      font=('Courier', 10, 'bold'),
                                      fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        explain_frame.pack(fill=tk.X, pady=10)
        
        explain_text = """HOW CRIB DRAGGING WORKS:
1. Attacker obtains C1 ⊕ C2 = M1 ⊕ M2
2. Guesses a word (crib) that might appear in M1
3. XORs crib with C1⊕C2 to reveal possible text in M2
4. Repeats with different positions and cribs to gradually recover both messages"""
        
        explain_lbl = tk.Label(explain_frame, text=explain_text, font=('Consolas', 10),
                              fg='#00ffff', bg=self.bg_color, justify=tk.LEFT)
        explain_lbl.pack(padx=10, pady=10)
        
        # Attack simulation
        sim_frame = tk.LabelFrame(main_frame, text="🎮 INTERACTIVE CRIB DRAGGING SIMULATION", 
                                  font=('Courier', 10, 'bold'),
                                  fg=self.fg_color, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        sim_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Known XOR input
        xor_frame = tk.Frame(sim_frame, bg=self.bg_color)
        xor_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(xor_frame, text="C1 ⊕ C2 (hex):", font=('Courier', 10),
                fg=self.fg_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        self.xor_input = tk.Entry(xor_frame, width=50, font=('Consolas', 10),
                                  bg='#1a1a1a', fg='#00ff00')
        self.xor_input.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Crib input
        crib_frame = tk.Frame(sim_frame, bg=self.bg_color)
        crib_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(crib_frame, text="CRIB (guessed word):", font=('Courier', 10),
                fg=self.fg_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        self.crib_input = tk.Entry(crib_frame, width=30, font=('Consolas', 10),
                                   bg='#1a1a1a', fg='#00ff00')
        self.crib_input.pack(side=tk.LEFT, padx=5)
        
        tk.Label(crib_frame, text="Position:", font=('Courier', 10),
                fg=self.fg_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        self.position_input = tk.Entry(crib_frame, width=10, font=('Consolas', 10),
                                       bg='#1a1a1a', fg='#00ff00')
        self.position_input.insert(0, "0")
        self.position_input.pack(side=tk.LEFT, padx=5)
        
        tk.Button(sim_frame, text="🔍 DRAG CRIB", command=self.drag_crib,
                 font=('Courier', 10, 'bold'), bg=self.accent_color, fg='#0a0a0a',
                 activebackground='#ff8800').pack(pady=5)
        
        # Results
        self.crib_results = scrolledtext.ScrolledText(sim_frame, height=15, font=('Consolas', 10),
                                                      bg='#1a1a1a', fg='#ff6600')
        self.crib_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Example button
        tk.Button(sim_frame, text="📋 LOAD EXAMPLE", command=self.load_example,
                 font=('Courier', 10, 'bold'), bg='#333333', fg=self.fg_color).pack(pady=5)
    
    def load_example(self):
        # Create example with the same two messages
        msg1 = "ATTACK AT DAWN"
        msg2 = "RETREAT AT NIGHT"
        max_len = max(len(msg1), len(msg2))
        key = self.generate_random_key(max_len)
        c1, _ = self.encrypt_otp(msg1, key)
        c2, _ = self.encrypt_otp(msg2, key)
        xored = self.xor_strings(c1, c2)
        
        self.xor_input.delete(0, tk.END)
        self.xor_input.insert(0, xored.encode('utf-8').hex())
        
        self.crib_results.delete('1.0', tk.END)
        self.crib_results.insert('1.0', "Example loaded! Try guessing 'ATTACK' at position 0\n")
        self.crib_results.insert(tk.END, f"Original messages used: '{msg1}' and '{msg2}'\n")
    
    def drag_crib(self):
        xor_hex = self.xor_input.get().strip()
        crib = self.crib_input.get().strip()
        
        try:
            pos = int(self.position_input.get())
        except:
            messagebox.showerror("Error", "Invalid position!")
            return
        
        if not xor_hex or not crib:
            messagebox.showerror("Error", "Please provide XOR value and crib!")
            return
        
        try:
            # Convert hex to string
            xored_bytes = bytes.fromhex(xor_hex)
            xored_str = xored_bytes.decode('utf-8', errors='ignore')
        except:
            messagebox.showerror("Error", "Invalid hex string!")
            return
        
        # Apply crib at specified position
        if pos + len(crib) > len(xored_str):
            self.crib_results.insert(tk.END, f"\n⚠️ Crib too long for position {pos}!\n")
            return
        
        # XOR crib with the XOR string to get the corresponding text in the other message
        result_chars = []
        for i in range(len(crib)):
            if pos + i < len(xored_str):
                result_char = chr(ord(xored_str[pos + i]) ^ ord(crib[i]))
                result_chars.append(result_char)
        
        result = ''.join(result_chars)
        
        self.crib_results.insert(tk.END, f"\n{'='*60}\n")
        self.crib_results.insert(tk.END, f"📍 CRIB DRAGGING AT POSITION {pos}\n")
        self.crib_results.insert(tk.END, f"{'='*60}\n")
        self.crib_results.insert(tk.END, f"Guessed crib: '{crib}'\n")
        self.crib_results.insert(tk.END, f"Revealed text in other message: '{result}'\n\n")
        
        # Check if result looks like English
        if all(c.isalpha() or c == ' ' for c in result):
            self.crib_results.insert(tk.END, "✅ Result appears to be valid text! This crib is likely correct.\n")
        else:
            self.crib_results.insert(tk.END, "⚠️ Result contains non-alphabetic characters. Try different crib.\n")
        
        self.crib_results.see(tk.END)
    
    # ==================== TAB 4: PRACTICAL LIMITATIONS ====================
    def setup_practical_limitations(self):
        text_frame = tk.Frame(self.tab4, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        security_text = scrolledtext.ScrolledText(text_frame, height=35, font=('Consolas', 10),
                                                  bg='#1a1a1a', fg='#ff6600')
        security_text.pack(fill=tk.BOTH, expand=True)
        
        security_content = """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║              🔐 ONE-TIME PAD: THEORETICAL PERFECTION vs PRACTICAL REALITY 🔐             ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝

📌 QUESTION: OTP is theoretically perfect but practically unusable. What are the obstacles?
═══════════════════════════════════════════════════════════════════════════════════════════

🚨 OBSTACLE 1: KEY GENERATION AND DISTRIBUTION
───────────────────────────────────────────────────────────────────────────────────────────
• PROBLEM: Need truly random key as long as the message
• CHALLENGE: Generating true randomness is expensive and slow
• QUANTUM RNG: Expensive equipment needed
• PRACTICAL ISSUE: Distributing gigabytes of key material securely

Example: 
  - Encrypting 1GB of data needs 1GB of random key
  - Transferring 1GB securely is as hard as sending the original data!

🚨 OBSTACLE 2: KEY MANAGEMENT NIGHTMARE
───────────────────────────────────────────────────────────────────────────────────────────
• Each pair of communicating parties needs a unique key
• For n parties: Need n(n-1)/2 unique keys
• With 1000 users: 499,500 different keys needed!
• Keys cannot be reused → must be discarded after use

┌──────────────┬──────────────────┬─────────────────────────────────────┐
│ Users (n)    │ Keys Required    │ Storage (1KB key per user pair)     │
├──────────────┼──────────────────┼─────────────────────────────────────┤
│ 2            │ 1                │ 1 KB                                │
│ 10           │ 45               │ 45 KB                               │
│ 100          │ 4,950            │ 4.95 MB                             │
│ 1,000        │ 499,500          │ 499 MB                              │
│ 10,000       │ 49,995,000       │ 49 GB                               │
│ 1,000,000    │ 499,999,500,000  │ 499 TB                              │└──────────────┴──────────────────┴─────────────────────────────────────┘

🚨 OBSTACLE 3: KEY SYNCHRONIZATION
───────────────────────────────────────────────────────────────────────────────────────────
• Both parties must have identical keys at the same position
• If keys get out of sync, communication fails
• No built-in error correction or recovery
• Lost key = permanently lost messages

🚨 OBSTACLE 4: AUTHENTICATION
───────────────────────────────────────────────────────────────────────────────────────────
• OTP provides confidentiality, NOT authentication
• An attacker can flip bits without detection
• Needs separate authentication system (MAC)
• Adds complexity and overhead

🚨 OBSTACLE 5: KEY STORAGE SECURITY
───────────────────────────────────────────────────────────────────────────────────────────
• Keys must be stored securely on both ends
• Any compromise of stored keys = all past/future messages compromised
• Protecting millions of keys is extremely difficult
• Physical security required (couriers, locked rooms, etc.)

🚨 OBSTACLE 6: REAL-TIME COMMUNICATION
───────────────────────────────────────────────────────────────────────────────────────────
• Cannot use for streaming or real-time communication
• Need pre-distributed keys for every possible message
• Not practical for internet-scale communication
• HTTPS, WhatsApp, Signal would be impossible

🚨 OBSTACLE 7: QUANTUM COMPUTING (IRONY!)
───────────────────────────────────────────────────────────────────────────────────────────
• OTP is quantum-resistant (perfect secrecy)
• BUT quantum key distribution (QKD) solves distribution
• QKD is extremely expensive and limited distance
• Not practical for global communication

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ WHERE OTP IS ACTUALLY USED:
───────────────────────────────────────────────────────────────────────────────────────────
1. • Diplomatic "red telephone" between Washington-Moscow (Cold War)
2. • Military special forces (short, critical messages)
3. • Some government intelligence operations
4. • Backup for quantum key distribution experiments

❌ WHERE OTP CANNOT BE USED:
───────────────────────────────────────────────────────────────────────────────────────────
1. • Internet browsing (HTTPS) - too many users, too much data
2. • Streaming services (Netflix, YouTube) - impossible key distribution
3. • Mobile communications (too many users, constant key renewal)
4. • Cloud storage (gigabytes of data, no secure key distribution)
5. • Email (asynchronous, key management impossible)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CONCLUSION: THEORETICAL PERFECTION vs PRACTICAL IMPOSSIBILITY
───────────────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────┐
│  PROPERTY              │ PERFECT SECRECY? │ PRACTICAL?                     │
├────────────────────────┼──────────────────┼────────────────────────────────┤
│  Confidentiality       │ YES ✓            │ Limited - key distribution     │
│  Authentication        │ NO ✗             │ NO - needs MAC                 │
│  Key distribution      │ Impossible       │ Extremely difficult           │
│  Key management        │ N/A              │ Nightmare for >10 users        │
│  Real-time use         │ N/A              │ NO - needs pre-shared keys     │
│  Internet scale        │ N/A              │ IMPOSSIBLE                     │
│  Error recovery        │ N/A              │ NO - stateless                 │
└─────────────────────────────────────────────────────────────────────────────┘

💡 FINAL VERDICT:
───────────────────────────────────────────────────────────────────────────────────────────
One-Time Pad is the ONLY mathematically proven unbreakable cipher (Shannon's theorem).
However, the key distribution problem makes it IMPRACTICAL for any real-world application
beyond tiny, ultra-secure, short-message scenarios.

Modern cryptography uses computational security (AES, ChaCha20) which is:
  ✓ Practically secure (no known efficient attacks)
  ✓ Easy key distribution (short keys: 128/256 bits)
  ✓ Efficient for any message length
  ✗ Not perfectly secure (theoretically breakable with unlimited resources)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                         ⚡ V E R N A M   S E C U R I T Y   A N A L Y S I S ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        security_text.insert('1.0', security_content)
        security_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = VernamOneTimePad(root)
    root.mainloop()

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║     V E R N A M   O N E - T I M E   P A D   S Y S T E M          ║
    ║                                                                   ║
    ║     Features:                                                     ║
    ║     ✓ Perfect secrecy (XOR-based encryption)                     ║
    ║     ✓ Random key generation                                      ║
    ║     ✓ Key reuse vulnerability demonstration                      ║
    ║     ✓ Crib dragging attack simulation                            ║
    ║     ✓ Practical limitations analysis                             ║
    ║                                                                   ║
    ║     Starting GUI...                                              ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    main()