"""Infinity Healthcare Test Search - desktop preview/test app.
Uses only Python's standard library (Tkinter + SQLite). Does not modify main.py.
Run: python app.py
"""
import os, sqlite3, tkinter as tk
from tkinter import ttk, messagebox

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, 'tests.db')
NAVY = '#102039'; TEAL = '#078f8b'; BG = '#f2f5f8'; TEXT = '#1b2938'; MUTED = '#647386'; WHITE = '#ffffff'
FIELDS = [('code','Test Code'),('test_name','Test Name'),('specimen','Specimen'),('reporting_time','Reporting Time'),('price','Price'),('b2b','B2B Price')]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mani Labs Solution')
        self.geometry('1120x720'); self.minsize(850,560); self.configure(bg=BG)
        if not os.path.exists(DB):
            messagebox.showerror('Database missing', 'tests.db was not found. Keep app.py and tests.db in the same folder.'); self.destroy(); return
        self.conn = sqlite3.connect(DB); self.conn.row_factory = sqlite3.Row
        self.selected_id = None; self.build_ui(); self.refresh()
        self.protocol('WM_DELETE_WINDOW', self.close)

    def build_ui(self):
        header=tk.Frame(self,bg=NAVY,height=100); header.pack(fill='x'); header.pack_propagate(False)
        left=tk.Frame(header,bg=NAVY); left.pack(side='left',fill='both',expand=True,padx=24,pady=17)
        tk.Label(left,text='MANI LABS SOLUTION',bg=NAVY,fg=WHITE,font=('Segoe UI',20,'bold')).pack(anchor='w')
        tk.Label(left,text='LAB TEST DIRECTORY  •  OFFLINE SEARCH',bg=NAVY,fg='#8fe0dc',font=('Segoe UI',10,'bold')).pack(anchor='w',pady=(4,0))
        tk.Button(header,text='+  ADD TEST',command=lambda:self.editor(),bg=TEAL,fg=WHITE,activebackground='#067b78',activeforeground=WHITE,relief='flat',font=('Segoe UI',10,'bold'),padx=18,pady=11,cursor='hand2').pack(side='right',padx=24)
        body=tk.Frame(self,bg=BG); body.pack(fill='both',expand=True,padx=22,pady=18)
        searchrow=tk.Frame(body,bg=WHITE,highlightbackground='#dce3e9',highlightthickness=1); searchrow.pack(fill='x',pady=(0,12))
        tk.Label(searchrow,text='⌕',bg=WHITE,fg=TEAL,font=('Segoe UI',24)).pack(side='left',padx=(14,7))
        self.query=tk.StringVar(); ent=tk.Entry(searchrow,textvariable=self.query,bd=0,bg=WHITE,fg=TEXT,insertbackground=TEAL,font=('Segoe UI',14)); ent.pack(side='left',fill='x',expand=True,ipady=13,padx=(0,8)); ent.insert(0,''); ent.bind('<KeyRelease>',lambda e:self.refresh()); ent.focus_set()
        tk.Button(searchrow,text='CLEAR',command=lambda:(self.query.set(''),self.refresh()),bg=WHITE,fg=MUTED,relief='flat',font=('Segoe UI',9,'bold'),padx=12,cursor='hand2').pack(side='right',padx=8)
        bar=tk.Frame(body,bg=BG); bar.pack(fill='x',pady=(0,8))
        self.count=tk.Label(bar,text='',bg=BG,fg=MUTED,font=('Segoe UI',10,'bold')); self.count.pack(side='left')
        tk.Label(bar,text='SELECT A TEST TO VIEW OR EDIT DETAILS',bg=BG,fg=MUTED,font=('Segoe UI',9)).pack(side='right')
        content=tk.Frame(body,bg=BG); content.pack(fill='both',expand=True)
        tableframe=tk.Frame(content,bg=WHITE,highlightbackground='#dce3e9',highlightthickness=1); tableframe.pack(side='left',fill='both',expand=True)
        cols=('code','test_name','reporting_time','price','b2b')
        self.tree=ttk.Treeview(tableframe,columns=cols,show='headings',selectmode='browse')
        names={'code':'CODE','test_name':'TEST NAME','reporting_time':'REPORTING TIME','price':'PRICE','b2b':'B2B'}
        widths={'code':90,'test_name':330,'reporting_time':165,'price':90,'b2b':80}
        for c in cols:self.tree.heading(c,text=names[c]); self.tree.column(c,width=widths[c],minwidth=65,anchor='w' if c in ('test_name','reporting_time') else 'center')
        vs=ttk.Scrollbar(tableframe,orient='vertical',command=self.tree.yview); self.tree.configure(yscrollcommand=vs.set); self.tree.pack(side='left',fill='both',expand=True); vs.pack(side='right',fill='y')
        self.tree.bind('<<TreeviewSelect>>',self.show_detail); self.tree.bind('<Double-1>',lambda e:self.edit_selected())
        style=ttk.Style(); style.theme_use('clam'); style.configure('Treeview',background=WHITE,fieldbackground=WHITE,foreground=TEXT,rowheight=34,font=('Segoe UI',10),borderwidth=0); style.configure('Treeview.Heading',background='#e8eef2',foreground=NAVY,font=('Segoe UI',9,'bold'),relief='flat'); style.map('Treeview',background=[('selected','#d8f0ef')],foreground=[('selected',NAVY)])
        detail=tk.Frame(content,bg=WHITE,width=300,highlightbackground='#dce3e9',highlightthickness=1); detail.pack(side='right',fill='y',padx=(12,0)); detail.pack_propagate(False)
        tk.Label(detail,text='TEST DETAILS',bg=WHITE,fg=NAVY,font=('Segoe UI',13,'bold')).pack(anchor='w',padx=17,pady=(18,4))
        tk.Frame(detail,bg=TEAL,height=3,width=52).pack(anchor='w',padx=17,pady=(0,13))
        self.detail_vars={}
        for key,label in FIELDS:
            block=tk.Frame(detail,bg=WHITE); block.pack(fill='x',padx=17,pady=5)
            tk.Label(block,text=label.upper(),bg=WHITE,fg=MUTED,font=('Segoe UI',8,'bold')).pack(anchor='w')
            v=tk.StringVar(value='—'); self.detail_vars[key]=v
            tk.Label(block,textvariable=v,bg=WHITE,fg=TEXT,font=('Segoe UI',10),wraplength=255,justify='left',anchor='w').pack(fill='x',anchor='w',pady=(2,0))
        actions=tk.Frame(detail,bg=WHITE); actions.pack(side='bottom',fill='x',padx=15,pady=15)
        tk.Button(actions,text='EDIT TEST',command=self.edit_selected,bg=TEAL,fg=WHITE,relief='flat',font=('Segoe UI',10,'bold'),pady=10,cursor='hand2').pack(fill='x',pady=(0,7))
        tk.Button(actions,text='DELETE TEST',command=self.delete_selected,bg='#fff0f0',fg='#a62d36',relief='flat',font=('Segoe UI',9,'bold'),pady=9,cursor='hand2').pack(fill='x')
        tk.Label(self,text='Powered by Mani 0322-7022841  •  OFFLINE DATABASE',bg=BG,fg='#8793a0',font=('Segoe UI',8)).pack(anchor='w',padx=24,pady=(0,9))

    def refresh(self):
        if not hasattr(self,'tree'): return
        q=self.query.get().strip().replace('*','')
        for item in self.tree.get_children(): self.tree.delete(item)
        if q:
            rows=self.conn.execute("SELECT id,code,test_name,reporting_time,price,b2b FROM tests WHERE code LIKE ? OR test_name LIKE ? COLLATE NOCASE ORDER BY test_name LIMIT 1000",(f'%{q}%',f'%{q}%')).fetchall()
        else: rows=self.conn.execute('SELECT id,code,test_name,reporting_time,price,b2b FROM tests ORDER BY test_name LIMIT 1000').fetchall()
        for r in rows:self.tree.insert('', 'end', iid=str(r['id']), values=(r['code'],r['test_name'],r['reporting_time'] or '',r['price'] or '',r['b2b'] or ''))
        total=self.conn.execute('SELECT COUNT(*) FROM tests').fetchone()[0]
        self.count.config(text=f'{len(rows)} MATCHING TESTS  •  {total} TOTAL RECORDS')
        if not rows:self.clear_detail()

    def clear_detail(self):
        self.selected_id=None
        for v in self.detail_vars.values():v.set('—')

    def show_detail(self,event=None):
        sel=self.tree.selection()
        if not sel:return
        self.selected_id=int(sel[0]); r=self.conn.execute('SELECT * FROM tests WHERE id=?',(self.selected_id,)).fetchone()
        if r:
            for key,_ in FIELDS:self.detail_vars[key].set(r[key] or '—')

    def edit_selected(self):
        sel=self.tree.selection()
        if not sel: messagebox.showinfo('Select a test','Please select a test first.'); return
        r=self.conn.execute('SELECT * FROM tests WHERE id=?',(int(sel[0]),)).fetchone(); self.editor(dict(r))

    def editor(self,record=None):
        win=tk.Toplevel(self); win.title('Add Test' if record is None else 'Edit Test'); win.configure(bg=BG); win.resizable(False,False); win.transient(self); win.grab_set()
        tk.Label(win,text='ADD NEW TEST' if record is None else 'EDIT TEST DETAILS',bg=NAVY,fg=WHITE,font=('Segoe UI',14,'bold'),padx=20,pady=15).pack(fill='x')
        form=tk.Frame(win,bg=BG); form.pack(padx=22,pady=18)
        vars={}
        for i,(key,label) in enumerate(FIELDS):
            tk.Label(form,text=label,bg=BG,fg=TEXT,font=('Segoe UI',10,'bold')).grid(row=i,column=0,sticky='w',pady=6,padx=(0,15))
            v=tk.StringVar(value=(record.get(key) or '') if record else ''); vars[key]=v
            ent=tk.Entry(form,textvariable=v,width=48,font=('Segoe UI',10),relief='solid',bd=1); ent.grid(row=i,column=1,sticky='ew',ipady=5,pady=5)
        buttons=tk.Frame(win,bg=BG); buttons.pack(fill='x',padx=22,pady=(0,18))
        def save():
            code=vars['code'].get().strip(); name=vars['test_name'].get().strip()
            if not code or not name:messagebox.showwarning('Required fields','Test Code and Test Name are required.',parent=win);return
            values=[vars[k].get().strip() for k,_ in FIELDS]
            try:
                if record:
                    self.conn.execute('UPDATE tests SET code=?,test_name=?,specimen=?,reporting_time=?,price=?,b2b=?,updated_at=CURRENT_TIMESTAMP WHERE id=?',(*values,record['id']))
                else:self.conn.execute('INSERT INTO tests(code,test_name,specimen,reporting_time,price,b2b) VALUES(?,?,?,?,?,?)',values)
                self.conn.commit(); win.destroy(); self.refresh()
                target=self.conn.execute('SELECT id FROM tests WHERE code=? ORDER BY id DESC LIMIT 1',(code,)).fetchone()
                if target and self.tree.exists(str(target['id'])):self.tree.selection_set(str(target['id']));self.tree.see(str(target['id']));self.show_detail()
            except sqlite3.Error as e:messagebox.showerror('Database error',str(e),parent=win)
        tk.Button(buttons,text='CANCEL',command=win.destroy,bg='#e3e8ed',fg=TEXT,relief='flat',font=('Segoe UI',10,'bold'),padx=18,pady=10).pack(side='right',padx=(8,0))
        tk.Button(buttons,text='SAVE TEST',command=save,bg=TEAL,fg=WHITE,relief='flat',font=('Segoe UI',10,'bold'),padx=20,pady=10).pack(side='right')

    def delete_selected(self):
        if not self.selected_id:messagebox.showinfo('Select a test','Please select a test first.');return
        name=self.detail_vars['test_name'].get()
        if messagebox.askyesno('Delete test',f'Delete "{name}" from this database? This cannot be undone.'):
            self.conn.execute('DELETE FROM tests WHERE id=?',(self.selected_id,));self.conn.commit();self.clear_detail();self.refresh()

    def close(self):
        self.conn.close(); self.destroy()

if __name__=='__main__':
    app=App(); app.mainloop()
