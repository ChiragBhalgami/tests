/************************************************************
** NOMAD: main program for ODBC-SQL-TMF Transaction Generator
*************************************************************
**
** This program will perform a selected set of actions on one
** to several SQL tables.  It is designed to be run by several
** processes under the control of a master process (NomadMaster)
**
** This program uses a specially formatted infile to determine which
** tables to use and what actions to perform.  This infile can be
** modified by hand with a text editor but, is normally
** generated by the master process, NomadMaster, which will provide the
** user-friendly interface.
**
** NOTE: All throughout the various source files the symbols '>>>'
**       are used to mark places where things are missing or need to
**       be eventually changed for the final version of this program.
**
** >>>refer to user's guide for more details (which isn't written yet)
**
*************************************************************/

#include "defines.h"
#include "include.h"
#include "bitlib.h"
#include "table.h"
#include "struct.h"
#include "sqlutil.h"
#include "status.h"
#include "ODBCcommon.h"

//=======================
// External declarations
//=======================
extern short adjust_percents(void);
extern void execute_by_percent(time_t run_time);
extern void execute_by_action(short action_type,short action_count);
extern short get_commands(void);

/***********/
/* Globals */
/***********/
#include "globals.c"

/**********************************************************************
** initialize
**
** This function sets the value of a few globals and opens and initializes
** the required files (for now the status file).
**********************************************************************/
short initialize()
{
   FILE *fp;
   time_t temp;

   /* set global start time */
   g_start_time=time(NULL);

   /* initialize global counters */
   g_action_count=0;
   g_trans_commit=0;
   g_trans_abort=0;

   /* create the status file */
   fp=fopen(g_status_file,"w");
   if(fp==NULL){
      LogMsg(ERRMSG+LINES,
             "unable to open status file '%s' for write access\n",
             g_status_file);
      return(FAILURE);
      }
   temp=time(NULL);
   fprintf(fp,"%s Status File initialized\n",ctime(&temp));
   fclose(fp);

   // initialize the global SQL data type info linked list
   gpSQLTypeInfoList=GetSQLTypeInfo(gDataSource,gUID,gPWD);
   if(gpSQLTypeInfoList==NULL) return(FAILURE);

   return(SUCCESS);
   } /* end initialize() */

/**********************************************************************
** get_table_info
**
** This function fills in the needed information into the array of table
** descriptions.
**********************************************************************/
short get_table_info(table_description *table_ptr[],short table_count)
{
   short i;
   ReturnStatus *RSPtr;
	HENV	henv;
	HDBC	hdbc;
	HSTMT hstmt;
	Boolean connected;
	RETCODE rc;

	RSPtr=NULL;
	// start a connection so we can use it to get the table info
	connected=FullConnect(gDataSource,gUID,gPWD,&henv,&hdbc);
	if(!connected) return(FAILURE);
	rc=SQLAllocStmt(hdbc,&hstmt);
	//>>>> check return code ???

   /* for each table, determine its format */
   for(i=0;i<table_count;i++){

      /* get format of table records, including column names */
      if(table_ptr[i]->Organization==KEY_SEQ){
         table_ptr[i]->pTable=GetTableInfo(hdbc,table_ptr[i]->TableName,FALSE,&RSPtr);
         }
      else{
         table_ptr[i]->pTable=GetTableInfo(hdbc,table_ptr[i]->TableName,TRUE,&RSPtr);
         }

      if(table_ptr[i]->pTable==NULL) {
			LogReturnStatus(RSPtr);
			FreeReturnStatus(RSPtr);
			return(FAILURE);
			}
		else{
			table_ptr[i]->henv=NULL;
			table_ptr[i]->hdbc=NULL;
			table_ptr[i]->hstmt=NULL;
			}
      }

	FullDisconnect(henv,hdbc);
   return(SUCCESS);
   } /* end of get_table_info() */



/**********************************************************************
** execute_command_list()
**
** This function is recursive.  It steps through the commands in the
** command list passed to it.  If the command list contains another
** command list (as is the case with nested loops) then it will call
** itself to execute that command list.  It will also propogate the
** time limits (if any) from the outer most loop.  So, a sub-loop with
** a time limit of 15 minutes within an outer loop with a time limit
** of only 10 minutes would not execute longer than the time limit of
** outer loop's time limit of 10 minutes.
**********************************************************************/
short execute_command_list(short list_num,time_t time_limit)
{
   short error;
   time_t run_time;
   time_t elapsed_time;
   time_t start_time;
   list_desc *l_ptr;
   Boolean done;
   Boolean done2;
   short i,j;
   short iterations;

   l_ptr=gpList[list_num];

   post_status(OK);

   /* see if someone has told us to stop */
   check_for_stop();

   start_time=time(NULL);

   /* adjust <run_time> to minimum of our <time_limit> or list's duration */
   run_time=l_ptr->duration;
   if(run_time>0) run_time*=60;
   if(time_limit>0){
      if((run_time<0)||(run_time>time_limit)) run_time=time_limit;
      }

   iterations=0;
   done=FALSE;
   while(!done){

      i=0;
      done2=FALSE;
      while(!done2){

         /* see if it is a list of percentages */
         if(l_ptr->item[i].code>0) {
            for(j=0;j<MAX_ACTION_TYPES;j++) g_percent[j]=NOT_SPECIFIED;
            for(j=0;j<l_ptr->item_count;j++) {
               g_percent[l_ptr->item[j].code]=l_ptr->item[j].u1.percentage;
               i++;
               }
            i--;
            if(adjust_percents()==FAILURE) return(FAILURE);
            execute_by_percent(run_time);
            }

         /* if a loop code then execute command list for the loop... */
         /* ...recursively */
         else if(l_ptr->item[i].code==0) {
            error=execute_command_list(l_ptr->item[i].u1.loop_number,run_time);
            /*>>> handle error somehow */
            }

         /* if an action code then go do action for 'n' repetitions */
         else if(l_ptr->item[i].code<0) {
            execute_by_action(l_ptr->item[i].code,
                              l_ptr->item[i].u1.repetitions);
            }

         /* see if someone has told us to stop */
         post_status(OK);
         check_for_stop();

         /* check if we've reached our stop time or end of item list */
         if(run_time>0) {
            elapsed_time=(time_t)difftime(time(NULL),start_time);
            if(elapsed_time>run_time) done2=TRUE;
            }
         else{
            i++;
            if(i>=l_ptr->item_count) done2=TRUE;
            }
         } /* end of while(!done2) */

      /* see if someone has told us to stop */
      post_status(OK);
      check_for_stop();

      /* check if we've reached our stop time or end of iterations */
      if(run_time>0) {
         elapsed_time=(time_t)difftime(time(NULL),start_time);
         if(elapsed_time>run_time) done=TRUE;
         }
      if(l_ptr->duration<0){
         iterations++;
         if(l_ptr->duration+iterations>=0) done=TRUE;
         }
      } /* end of while(!done) */

   return(0);
   } /* end of execute_command_list() */


/****************/
/* Main Program */
// argv[1] = process number
// argv[2] = command file
// argv[3] = log file
/****************/
int main(int argc,char *argv[])
{
   short error;                /* general purpose error variable */
   int pid;

   gProcessNumber = atoi(argv[1]);
   gPid = getpid();
   printf("Worker Process %03d is now running.  Pid=%d  Logfile=%s.\n",
	   gProcessNumber,gPid,argv[3]);

   // get name of input command file which will be remapped to STDIN
   // all parms and commands are input through stdin file
   strcpy(gCommandFile,argv[2]);

   /* open a log file */
   LogInit(argv[3],5);

   /* print header */
   LogMsg(LINEAFTER,"ODBC/SQL/TM Query/Transaction Generator (NOMAD)\n"
                    "Compiled: %s  %s\n\n",
                    __DATE__,__TIME__);

   /* read in command file contents and see what we're supposed to do */
   if(get_commands()!=SUCCESS) exit(EXIT_FAILURE);

   LogMsg(LINEAFTER,"MasterSeed = %d\n",gMasterSeed);

   /* initialize some globals, find and open required files */
   if(initialize()!=0) exit(EXIT_FAILURE);

   post_status(STARTED);

   /* get needed info about each of the tables this process will use */
   if(get_table_info(gpTableDesc,(short)gTableCount)!=0) exit(EXIT_FAILURE);

   /* now start the main execution loop */
   error=execute_command_list(0,gpList[0]->duration);
   /*>>> handle error somehow */
   /*>>> may not be a need to handle errors if it already posts... */
   /*>>>...error messages to the logfile */

   post_status(FINISHED);

   /* perform any clean up */
   /*>>> there currently isn't anything to do for clean-up, but later... */
   /*>>> ...versions will support this option */

	exit(EXIT_SUCCESS);
   } /* end of main() */
