#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

/*
---------------------------------------------------------
   TestSQLAllocEnv: Test SQLAllocEnv and SQLFreeEnv
---------------------------------------------------------
*/

PassFail TestSQLAllocEnv(TestInfo *pTestInfo)

{ 
	
	TEST_DECLARE;
  RETCODE returncode;
  SQLHANDLE henv;
  SQLHANDLE OldHenv;
  SQLHANDLE BadHenv;       
   
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLAllocEnvirnoment.\n"));

	TEST_INIT;
	   
  TESTCASE_BEGIN("Test basic functionality of SQLAllocEnv\n");
  henv=(SQLHANDLE)NULL;
  returncode = SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
      /* Fatal error, no use running the remaining tests so, return */
		TEST_FAILED;
		TEST_RETURN;
  }
  TESTCASE_END;
   
  TESTCASE_BEGIN("Test non-NULL handle value\n");
  OldHenv=henv;
  returncode=SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
	{
     SQLFreeEnv(OldHenv);
     LogMsg(ENDLINE,_T("Using a valid, non-NULL handle caused an error.\n"));
    /* Fatal error, no use running the remaining tests so, return */
    TEST_FAILED;
		TEST_RETURN;
  }
  TESTCASE_END;
   
  TESTCASE_BEGIN("Negative test: Invalid handle pointer\n");
  BadHenv=(SQLHANDLE)NULL;
  returncode=SQLAllocEnv((SQLHANDLE *)BadHenv);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLAllocEnv"))
	{
	   LogMsg(ENDLINE,_T("Invalid handle pointer works, it shouldn't.\n"));
	   TEST_FAILED;
	}
  TESTCASE_END;

  TESTCASE_BEGIN("Test basic functionality of SQLFreeEnv\n");
  returncode=SQLFreeEnv(OldHenv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv"))
	{
    LogAllErrors(OldHenv,(SQLHANDLE)NULL,(SQLHANDLE)NULL);
		TEST_FAILED;
	}
      
  returncode=SQLFreeEnv(henv);   
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv"))
	{
    LogAllErrors(henv,(SQLHANDLE)NULL,(SQLHANDLE)NULL);
	  TEST_FAILED;
	}
  TESTCASE_END;
   
/*	// this is a bug in driver manager we cannot free already freed   
	TESTCASE_BEGIN("Negative test: free an already freed handle\n");
	returncode=SQLFreeEnv(henv);   
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLFreeEnv"))
	{
		LogMsg(ENDLINE,"Invalid handle didn't produce proper error.");
    TEST_FAILED
	}

	TESTCASE_END;
*/

	LogMsg(SHORTTIMESTAMP+LINEBEFORE+LINEAFTER,_T("End testing API => SQLAllocEnvirnoment.\n"));
  TEST_RETURN;

}
