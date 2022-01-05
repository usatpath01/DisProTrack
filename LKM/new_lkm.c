#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <asm/current.h>
#include <asm/ptrace.h>
#include <linux/sched.h>
#include <linux/cred.h>
#include <asm/unistd.h>
#include <linux/spinlock.h>
#include <linux/semaphore.h>
#include <linux/syscalls.h>
#include <linux/kallsyms.h>

#define FDPUT_FPUT       1
#define FDPUT_POS_UNLOCK 2
#define FMODE_ATOMIC_POS    ((__force fmode_t)0x8000)

MODULE_DESCRIPTION("My kernel module");
MODULE_AUTHOR("Me");
MODULE_LICENSE("GPL");

// static void **sys_call_table;
unsigned long sys_call_table_addr ;
typedef int (* syscall_wrapper)(struct pt_regs *);

syscall_wrapper original_write;

unsigned long __fdget_pos(unsigned int fd)
{
    unsigned long v = __fdget(fd);
    struct file *file = (struct file *)(v & ~3);

    if (file && (file->f_mode & FMODE_ATOMIC_POS)) {
        if (file_count(file) > 1) {
            v |= FDPUT_POS_UNLOCK;
            mutex_lock(&file->f_pos_lock);
        }
    }
    return v;
}

static inline loff_t *file_ppos(struct file *file)
{
    return file->f_mode & FMODE_STREAM ? NULL : &file->f_pos;
}


void __f_unlock_pos(struct file *f)
{
    mutex_unlock(&f->f_pos_lock);
}


static ssize_t my_ksys_write(unsigned int fd, const char __user *buf, size_t count)
{
    struct fd f = fdget_pos(fd);
    ssize_t ret = -EBADF;

    if (f.file) {
        loff_t pos, *ppos = file_ppos(f.file);
        if (ppos) {
            pos = *ppos;
            ppos = &pos;
        }
        ret = kernel_write(f.file, buf, count, ppos);
        if (ret >= 0 && ppos)
            f.file->f_pos = pos;
        fdput_pos(f);
    }

    return ret;
}


int sys_write_hook(struct pt_regs *regs)
{
	int fd = regs->di;

    struct file* get_file = NULL;
    struct fd get_file_pointer ;
    
    struct dentry *parent = NULL;
    int safe = 6,var_flag = 0,log_flag = 0,journal_flag = 0,unattended_flag = 0,installer_flag = 0;
    char var_cmp[] = "var";
    char log_cmp[] = "log";
    char journal_cmp[] = "journal";
    char unattended_cmp[] = "unattended-upgrades";
    char installer_cmp[] = "installer";
    int var_level = 0;
    int log_level = 0;
    int level = 0;

    long long totalsecs = 0;
    int pid = 0;
    int sz_tempstr = 0;
    char *tempstr = NULL;
    int ok=0;
    

   get_file_pointer = fdget_pos(fd);

   if(get_file_pointer.file)
    {   
        get_file = get_file_pointer.file;
        fdput_pos(get_file_pointer);        
        if(get_file && get_file->f_path.dentry!=NULL)
        {   
            parent = get_file->f_path.dentry->d_parent;
            while(safe-- && parent!=NULL)
            {
                if(strcmp(parent->d_name.name,var_cmp)==0)
                {   

                    var_flag = 1;
                    var_level = level;
                    break;
                }

                if(strcmp(parent->d_name.name,log_cmp)==0)
                {   
                    log_flag = 1;
                    log_level = level;
                }

                if(strcmp(parent->d_name.name,journal_cmp)==0)
                {   
                    journal_flag = 1;
                    break;
                }


                if(strcmp(parent->d_name.name,installer_cmp)==0)
                {   
                    installer_flag = 1;
                    break;
                }

                if(strcmp(parent->d_name.name,unattended_cmp)==0)
                {   
                    unattended_flag = 1;
                    break;
                }
                
                level++;

                if(strcmp(parent->d_name.name,"/")==0)
                    break;

                parent = parent->d_parent;
            }

            if(var_flag && log_flag && !journal_flag && !installer_flag
             && !unattended_flag && log_level>=1 && var_level>=2)
            {
                ok = 1;
                totalsecs = ktime_get_real_ns();
                pid = task_tgid_vnr(current);

                tempstr = (char*)(kmalloc(100*sizeof(char),GFP_KERNEL));
                if(!tempstr)
                    ok = 0;

                if(ok)
                {
                    sz_tempstr = snprintf(tempstr,100*sizeof(char), "pid = %d, date = [%lld] "
                    ,pid,totalsecs); 

                    if(sz_tempstr<0)
                        ok = 0;

                    if(ok)
                        my_ksys_write(fd, tempstr, sz_tempstr);
                }
                
                if(tempstr)
                    kfree(tempstr);
            }
        }
    }


   return (*original_write)(regs);

}

int set_addr_rw(void *ptr){
  unsigned int level;
  pte_t *pte = lookup_address((unsigned long) ptr, &level);
  if(pte->pte &~_PAGE_RW){
    pte->pte |=_PAGE_RW;
  }
  return 0;
}

int set_addr_ro(void *ptr){
  unsigned int level;
  pte_t *pte = lookup_address((unsigned long) ptr, &level);
  pte->pte = pte->pte &~_PAGE_RW;
  return 0;
}

static int init_function(void) 
{
	
	sys_call_table_addr = kallsyms_lookup_name("sys_call_table");

	set_addr_rw((void*)sys_call_table_addr);
	original_write = ((syscall_wrapper*)sys_call_table_addr)[__NR_write];
	((syscall_wrapper*)sys_call_table_addr)[__NR_write] = sys_write_hook;
	set_addr_ro((void*) sys_call_table_addr);	
	return 0;
}


static void exit_function(void) 
{


	set_addr_rw((void*) sys_call_table_addr);    
	((syscall_wrapper*)sys_call_table_addr)[__NR_write] = original_write;
	
	set_addr_ro((void*) sys_call_table_addr);
	printk(KERN_EMERG "Module exited cleanly");
	return;

}

module_init(init_function);
module_exit(exit_function);