/*************************************************************************
*
// @@@ START COPYRIGHT @@@
//
//  Copyright 1998
//  Compaq Computer Corporation
//     Protected as an unpublished work.
//        All rights reserved.
//
//  The computer program listings, specifications, and documentation
//  herein are the property of Compaq Computer Corporation or a
//  third party supplier and shall not be reproduced, copied,
//  disclosed, or used in whole or in part for any reason without
//  the prior express written permission of Compaq Computer
//  Corporation.
//
// @@@ END COPYRIGHT @@@ 
**************************************************************************/

#ifndef WINDOWS_H_
#define WINDOWS_H_
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <limits.h>
#include "unix_extra.h"

#ifdef unixcli
#ifndef NSK_PLATFORM
#define NSK_PLATFORM
#include <unistd.h>
#endif
#endif

#ifndef unixcli
#ifdef _YOSBUILD
#include "cextdecs.h"
#else
#include "cextdecs\cextdecs.h"
#endif
#endif

#ifdef __cplusplus
extern "C" { 			/* Assume C declarations for C++   */
#endif  /* __cplusplus */

#ifndef NULL
#define NULL 0
#endif

#ifndef false
#define false 0
#endif

#ifndef true
#define true 1
#endif

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif // !FALSE
#ifndef _BYTE_DEFINED
#define _BYTE_DEFINED
typedef unsigned char BYTE;

#endif // !_BYTE_DEFINED
#ifndef _WORD_DEFINED
#define _WORD_DEFINED
typedef unsigned short WORD;

#endif // !_WORD_DEFINED
typedef unsigned int UINT;

typedef int INT;

typedef char BOOL;

#ifndef _LONG_DEFINED
#define _LONG_DEFINED
typedef long LONG;

#endif // !_LONG_DEFINED
#ifndef _DWORD_DEFINED
#ifndef DWORD
typedef unsigned long DWORD;
#define _DWORD_DEFINED
#endif

#endif // !_DWORD_DEFINED
#ifndef _LRESULT_DEFINED
#define _LRESULT_DEFINED
typedef LONG LRESULT;

#endif // !_LRESULT_DEFINED

typedef char CHAR;

#ifndef unixcli
typedef unsigned char UCHAR;
#endif

typedef short SHORT;

#ifndef unixcli
typedef unsigned short USHORT;

typedef DWORD ULONG;
#endif

typedef double DOUBLE;

#ifndef unixcli
typedef long long __int64;
#endif

typedef float FLOAT;
typedef BOOL BOOLEAN;
typedef void* PVOID;
typedef PVOID HLOCAL;

#ifndef _HRESULT_DEFINED
#define _HRESULT_DEFINED
typedef LONG HRESULT;

#endif // !_HRESULT_DEFINED


// from WCTYPE.H
/* Define __cdecl for non-Microsoft compilers */

#if	( !defined(_MSC_VER) && !defined(__cdecl) )
#define __cdecl
#endif

#ifndef SYSTEMTIME
typedef struct _SYSTEMTIME {
	WORD wYear; 
	WORD wMonth; 
	WORD wDayOfWeek; 
	WORD wDay; 
	WORD wHour; 
	WORD wMinute; 
	WORD wSecond; 
	WORD wMilliseconds; 
} SYSTEMTIME;

#endif //SYSTEMTIME

#define CONST const

//from WINNT.H
//
// The types of events that can be logged.
//
#define EVENTLOG_SUCCESS                0X0000
#define EVENTLOG_ERROR_TYPE             0x0001
#define EVENTLOG_WARNING_TYPE           0x0002
#define EVENTLOG_INFORMATION_TYPE       0x0004
#define EVENTLOG_AUDIT_SUCCESS          0x0008
#define EVENTLOG_AUDIT_FAILURE          0x0010

// Registry Specific Access Rights.
//
#define SYNCHRONIZE                      (0x00100000L)
#define READ_CONTROL                     (0x00020000L)
#define STANDARD_RIGHTS_READ             (READ_CONTROL)

#define KEY_QUERY_VALUE         (0x0001)
#define KEY_SET_VALUE           (0x0002)
#define KEY_CREATE_SUB_KEY      (0x0004)
#define KEY_ENUMERATE_SUB_KEYS  (0x0008)
#define KEY_NOTIFY              (0x0010)
#define KEY_CREATE_LINK         (0x0020)

#define KEY_READ                ((STANDARD_RIGHTS_READ       |\
                                  KEY_QUERY_VALUE            |\
                                  KEY_ENUMERATE_SUB_KEYS     |\
                                  KEY_NOTIFY)                 \
                                  &                           \
                                 (~SYNCHRONIZE))

#define LANG_ENGLISH                     0x09
#define LANG_JAPANESE                    0x11
#define LANGIDFROMLCID(lcid)   ((WORD  )(lcid))
#define PRIMARYLANGID(lgid)    ((WORD  )(lgid) & 0x3ff)
#define SORT_DEFAULT                     0x0 
#define SUBLANG_NEUTRAL                  0x00

#define INFINITE				0xFFFFFFFF
#define STATUS_WAIT_0			((DWORD   )0x00000000L)  
#define WAIT_OBJECT_0			((STATUS_WAIT_0 ) + 0 )
/****************************************************/
// My RSSH added stuff, I'll check it later
// from MAPIWIN.H
// Critical section code
#ifndef CRITICAL_SECTION
#define CRITICAL_SECTION ULONG
#endif

#ifndef LPCRITICAL_SECTION
#define LPCRITICAL_SECTION ULONG *
#endif

#ifndef HINSTANCE
#define HINSTANCE int
#endif

#ifndef HANDLE
#define HANDLE int
#endif

#ifndef HMODULE
#define HMODULE int
#endif

#ifndef BYTE
#define BYTE char
#endif

#ifndef HWND
#define HWND int
#endif

#ifndef UINT
#define UINT	unsigned int
#endif

#ifndef WORD
#define WORD	int
#endif

#ifndef DWORD
#define DWORD	long
#endif

#ifndef LPCVOID
#define LPCVOID	void *
#endif

#ifndef PVOID
#define PVOID char *
#endif

#ifndef FARPROC
#define FARPROC long *
#endif

#if !defined(unixcli)
#ifndef TCHAR
#define TCHAR char
#endif
#endif

#ifndef VOID
#define VOID	void
#endif

// types from Windef.h
typedef DWORD *PDWORD;
typedef BYTE *PBYTE;
typedef BYTE *LPBYTE;
#ifndef unixcli
    #define far				_far
    #define FAR				_far
    typedef void far            *LPVOID;
#else
    typedef void	*LPVOID;
#endif


#ifndef max
#define max(a,b)            (((a) > (b)) ? (a) : (b))
#endif

#ifndef min
#define min(a,b)            (((a) < (b)) ? (a) : (b))
#endif

// types from WinTypes.h
typedef PVOID PSID;
typedef DWORD *LPDWORD;

typedef struct  _SECURITY_ATTRIBUTES
    {
    DWORD nLength;
    /* [size_is] */ LPVOID lpSecurityDescriptor;
    BOOL bInheritHandle;
    }	SECURITY_ATTRIBUTES;

//typedef struct _SECURITY_ATTRIBUTES __RPC_FAR *PSECURITY_ATTRIBUTES;

typedef struct _SECURITY_ATTRIBUTES *LPSECURITY_ATTRIBUTES;

typedef DWORD ( *PTHREAD_START_ROUTINE)(
    LPVOID lpThreadParameter
    );
typedef PTHREAD_START_ROUTINE LPTHREAD_START_ROUTINE;


// from WinNt.h
typedef DWORD ACCESS_MASK;
#ifndef WIN32_NO_STATUS 
/*lint -save -e767 */  
#define STATUS_WAIT_0                    ((DWORD   )0x00000000L)    
#define STATUS_ABANDONED_WAIT_0          ((DWORD   )0x00000080L)    
#define STATUS_USER_APC                  ((DWORD   )0x000000C0L)    
#define STATUS_TIMEOUT                   ((DWORD   )0x00000102L)    
#define STATUS_PENDING                   ((DWORD   )0x00000103L)    
#define STATUS_SEGMENT_NOTIFICATION      ((DWORD   )0x40000005L)    
#define STATUS_GUARD_PAGE_VIOLATION      ((DWORD   )0x80000001L)    
#define STATUS_DATATYPE_MISALIGNMENT     ((DWORD   )0x80000002L)    
#define STATUS_BREAKPOINT                ((DWORD   )0x80000003L)    
#define STATUS_SINGLE_STEP               ((DWORD   )0x80000004L)    
#define STATUS_ACCESS_VIOLATION          ((DWORD   )0xC0000005L)    
#define STATUS_IN_PAGE_ERROR             ((DWORD   )0xC0000006L)    
#define STATUS_INVALID_HANDLE            ((DWORD   )0xC0000008L)    
#define STATUS_NO_MEMORY                 ((DWORD   )0xC0000017L)    
#define STATUS_ILLEGAL_INSTRUCTION       ((DWORD   )0xC000001DL)    
#define STATUS_NONCONTINUABLE_EXCEPTION  ((DWORD   )0xC0000025L)    
#define STATUS_INVALID_DISPOSITION       ((DWORD   )0xC0000026L)    
#define STATUS_ARRAY_BOUNDS_EXCEEDED     ((DWORD   )0xC000008CL)    
#define STATUS_FLOAT_DENORMAL_OPERAND    ((DWORD   )0xC000008DL)    
#define STATUS_FLOAT_DIVIDE_BY_ZERO      ((DWORD   )0xC000008EL)    
#define STATUS_FLOAT_INEXACT_RESULT      ((DWORD   )0xC000008FL)    
#define STATUS_FLOAT_INVALID_OPERATION   ((DWORD   )0xC0000090L)    
#define STATUS_FLOAT_OVERFLOW            ((DWORD   )0xC0000091L)    
#define STATUS_FLOAT_STACK_CHECK         ((DWORD   )0xC0000092L)    
#define STATUS_FLOAT_UNDERFLOW           ((DWORD   )0xC0000093L)    
#define STATUS_INTEGER_DIVIDE_BY_ZERO    ((DWORD   )0xC0000094L)    
#define STATUS_INTEGER_OVERFLOW          ((DWORD   )0xC0000095L)    
#define STATUS_PRIVILEGED_INSTRUCTION    ((DWORD   )0xC0000096L)    
#define STATUS_STACK_OVERFLOW            ((DWORD   )0xC00000FDL)    
#define STATUS_CONTROL_C_EXIT            ((DWORD   )0xC000013AL)    
/*lint -restore */  
#endif //WIN32_NO_STATUS

// from WINBASE.H

#define WAIT_FAILED (DWORD)0xFFFFFFFF
#define WAIT_OBJECT_0       ((STATUS_WAIT_0 ) + 0 )

#define WAIT_ABANDONED         ((STATUS_ABANDONED_WAIT_0 ) + 0 )
#define WAIT_ABANDONED_0       ((STATUS_ABANDONED_WAIT_0 ) + 0 )

#define WAIT_TIMEOUT                        STATUS_TIMEOUT
#define WAIT_IO_COMPLETION                  STATUS_USER_APC
#define STILL_ACTIVE                        STATUS_PENDING
#define EXCEPTION_ACCESS_VIOLATION          STATUS_ACCESS_VIOLATION
#define EXCEPTION_DATATYPE_MISALIGNMENT     STATUS_DATATYPE_MISALIGNMENT
#define EXCEPTION_BREAKPOINT                STATUS_BREAKPOINT
#define EXCEPTION_SINGLE_STEP               STATUS_SINGLE_STEP
#define EXCEPTION_ARRAY_BOUNDS_EXCEEDED     STATUS_ARRAY_BOUNDS_EXCEEDED
#define EXCEPTION_FLT_DENORMAL_OPERAND      STATUS_FLOAT_DENORMAL_OPERAND
#define EXCEPTION_FLT_DIVIDE_BY_ZERO        STATUS_FLOAT_DIVIDE_BY_ZERO
#define EXCEPTION_FLT_INEXACT_RESULT        STATUS_FLOAT_INEXACT_RESULT
#define EXCEPTION_FLT_INVALID_OPERATION     STATUS_FLOAT_INVALID_OPERATION
#define EXCEPTION_FLT_OVERFLOW              STATUS_FLOAT_OVERFLOW
#define EXCEPTION_FLT_STACK_CHECK           STATUS_FLOAT_STACK_CHECK
#define EXCEPTION_FLT_UNDERFLOW             STATUS_FLOAT_UNDERFLOW
#define EXCEPTION_INT_DIVIDE_BY_ZERO        STATUS_INTEGER_DIVIDE_BY_ZERO
#define EXCEPTION_INT_OVERFLOW              STATUS_INTEGER_OVERFLOW
#define EXCEPTION_PRIV_INSTRUCTION          STATUS_PRIVILEGED_INSTRUCTION
#define EXCEPTION_IN_PAGE_ERROR             STATUS_IN_PAGE_ERROR
#define EXCEPTION_ILLEGAL_INSTRUCTION       STATUS_ILLEGAL_INSTRUCTION
#define EXCEPTION_NONCONTINUABLE_EXCEPTION  STATUS_NONCONTINUABLE_EXCEPTION
#define EXCEPTION_STACK_OVERFLOW            STATUS_STACK_OVERFLOW
#define EXCEPTION_INVALID_DISPOSITION       STATUS_INVALID_DISPOSITION
#define EXCEPTION_GUARD_PAGE                STATUS_GUARD_PAGE_VIOLATION
#define EXCEPTION_INVALID_HANDLE            STATUS_INVALID_HANDLE

#define MAX_COMPUTERNAME_LENGTH 15

//
// dwCreationFlag values
//

#define DEBUG_PROCESS               0x00000001
#define DEBUG_ONLY_THIS_PROCESS     0x00000002

#define CREATE_SUSPENDED            0x00000004

#define DETACHED_PROCESS            0x00000008

#define CREATE_NEW_CONSOLE          0x00000010

#define NORMAL_PRIORITY_CLASS       0x00000020
#define IDLE_PRIORITY_CLASS         0x00000040
#define HIGH_PRIORITY_CLASS         0x00000080
#define REALTIME_PRIORITY_CLASS     0x00000100

#define CREATE_NEW_PROCESS_GROUP    0x00000200
#define CREATE_UNICODE_ENVIRONMENT  0x00000400

#define CREATE_SEPARATE_WOW_VDM     0x00000800
#define CREATE_SHARED_WOW_VDM       0x00001000
#define CREATE_FORCEDOS             0x00002000

#define CREATE_DEFAULT_ERROR_MODE   0x04000000
#define CREATE_NO_WINDOW            0x08000000

#define PROFILE_USER                0x10000000
#define PROFILE_KERNEL              0x20000000
#define PROFILE_SERVER              0x40000000

#define THREAD_PRIORITY_LOWEST          THREAD_BASE_PRIORITY_MIN
#define THREAD_PRIORITY_BELOW_NORMAL    (THREAD_PRIORITY_LOWEST+1)
#define THREAD_PRIORITY_NORMAL          0
#define THREAD_PRIORITY_HIGHEST         THREAD_BASE_PRIORITY_MAX
#define THREAD_PRIORITY_ABOVE_NORMAL    (THREAD_PRIORITY_HIGHEST-1)
#define THREAD_PRIORITY_ERROR_RETURN    (MAXLONG)

#define THREAD_PRIORITY_TIME_CRITICAL   THREAD_BASE_PRIORITY_LOWRT
#define THREAD_PRIORITY_IDLE            THREAD_BASE_PRIORITY_IDLE

void 
OutputDebugString(
    char *lpOutputString
    );

BOOL
GetExitCodeThread(
    HANDLE hThread,
    LPDWORD lpExitCode
    );

HANDLE
CreateThread(
    LPSECURITY_ATTRIBUTES lpThreadAttributes,
    DWORD dwStackSize,
    LPTHREAD_START_ROUTINE lpStartAddress,
    LPVOID lpParameter,
    DWORD dwCreationFlags,
    LPDWORD lpThreadId
    );


DWORD
SuspendThread(
    HANDLE hThread
    );

DWORD
ResumeThread(
    HANDLE hThread
    );

DWORD
WaitForSingleObject(
    HANDLE hHandle,
    DWORD dwMilliseconds
    );

/*
typedef struct _SID_IDENTIFIER_AUTHORITY {
    BYTE  Value[6];
} SID_IDENTIFIER_AUTHORITY, *PSID_IDENTIFIER_AUTHORITY;

typedef struct _SID {
   BYTE  Revision;
   BYTE  SubAuthorityCount;
   SID_IDENTIFIER_AUTHORITY IdentifierAuthority;
#ifdef MIDL_PASS
   [size_is(SubAuthorityCount)] DWORD SubAuthority[*];
#else // MIDL_PASS
   DWORD SubAuthority[ANYSIZE_ARRAY];
#endif // MIDL_PASS
} SID, *PISID;

*/

/***************************************************/
// from WINERROR.H
//
//  The operation completed successfully.
//
#define ERROR_SUCCESS                    0L  
#define ERROR_NO_TOKEN                   1008L
#define ERROR_LOGON_FAILURE              1326L

// from MAPINLS.H
//
typedef unsigned short                  WCHAR;
typedef WCHAR FAR *                     LPWSTR;
//typedef const WCHAR FAR *               LPCWSTR;
//typedef CHAR FAR *                      LPSTR;
typedef CHAR * LPSTR;
//typedef const CHAR FAR *                LPCSTR;
//typedef TCHAR FAR *                     LPTSTR;
//typedef const TCHAR FAR *               LPCTSTR;
typedef const CHAR * LPCTSTR;
typedef const CHAR * LPCWSTR;
typedef DWORD                           LCID;
//typedef const void FAR *                LPCVOID;


// from y:\inc\cextdecs\cextdecs.h
//
//static short const          OMITSHORT         = -291;
//static int const            OMITINT           = -19070975;
#ifndef OMITREF
#define OMITREF     
#endif

#ifndef OMITSHORT
#define OMITSHORT     
#endif

#ifndef OMITINT
#define OMITINT     
#endif

// international character sets from WINRESRC.H
#define LANG_NEUTRAL                     0x00
#define SUBLANG_DEFAULT                  0x00
#define LPTSTR				char *
#define LPSTR				char *
#define LPCSTR				const char *
#define wsprintf	sprintf
#define TEXT

// Macros to process language values (from WINNT.H)
#define MAKELANGID(p, s)       ((((WORD  )(s)) << 10) | (WORD  )(p))
#define PRIMARYLANGID(lgid)    ((WORD  )(lgid) & 0x3ff)
#define SUBLANGID(lgid)        ((WORD  )(lgid) >> 10)
#define MAKELCID(lgid, srtid)  ((DWORD)((((DWORD)((WORD  )(srtid))) << 16) | ((DWORD)((WORD  )(lgid))))) 
typedef HANDLE * PHANDLE;

#ifndef NMBERFMT
#define NMBERFMT
typedef struct _numberfmtA {
    UINT    NumDigits;                 // number of decimal digits
    UINT    LeadingZero;               // if leading zero in decimal fields
    UINT    Grouping;                  // group size left of decimal
    LPSTR   lpDecimalSep;              // ptr to decimal separator string
    LPSTR   lpThousandSep;             // ptr to thousand separator string
    UINT    NegativeOrder;             // negative number ordering
} NUMBERFMT; 
 
#endif

/*
#define TOKEN_QUERY             (0x0008)

typedef struct _TOKEN_USER {
    SID_AND_ATTRIBUTES User;
} TOKEN_USER, *PTOKEN_USER;

typedef struct _TOKEN_OWNER {
    PSID Owner;
} TOKEN_OWNER, *PTOKEN_OWNER;

typedef enum _SID_NAME_USE {
    SidTypeUser = 1,
    SidTypeGroup,
    SidTypeDomain,
    SidTypeAlias,
    SidTypeWellKnownGroup,
    SidTypeDeletedAccount,
    SidTypeInvalid,
    SidTypeUnknown
} SID_NAME_USE, *PSID_NAME_USE;

typedef enum _TOKEN_INFORMATION_CLASS {
    TokenUser = 1,
    TokenGroups,
    TokenPrivileges,
    TokenOwner,
    TokenPrimaryGroup,
    TokenDefaultDacl,
    TokenSource,
    TokenType,
    TokenImpersonationLevel,
    TokenStatistics
} TOKEN_INFORMATION_CLASS, *PTOKEN_INFORMATION_CLASS;

typedef enum _TOKEN_TYPE {
    TokenPrimary = 1,
    TokenImpersonation
    } TOKEN_TYPE;
typedef TOKEN_TYPE *PTOKEN_TYPE;
*/

// from error.h
#define ERROR_INSUFFICIENT_BUFFER   122
#ifndef NO_ERROR
#define NO_ERROR            0
#endif
#define ERROR_FILE_NOT_FOUND        2


// Generic Format Message function from WINBASE.H
#define FORMAT_MESSAGE_ALLOCATE_BUFFER 0x00000100
#define FORMAT_MESSAGE_IGNORE_INSERTS  0x00000200
#define FORMAT_MESSAGE_FROM_STRING     0x00000400
#define FORMAT_MESSAGE_FROM_HMODULE    0x00000800
#define FORMAT_MESSAGE_FROM_SYSTEM     0x00001000
#define FORMAT_MESSAGE_ARGUMENT_ARRAY  0x00002000
#define FORMAT_MESSAGE_MAX_WIDTH_MASK  0x000000FF
#define LOGON32_LOGON_INTERACTIVE   2
#define LOGON32_PROVIDER_DEFAULT    0

FARPROC GetProcAddress(HMODULE hModule, LPCSTR lpProcName);
HMODULE LoadLibrary(LPCSTR lpLibFileName);
BOOL FreeLibrary( HMODULE hLibModule); 

//BOOL IsValidSid (PSID pSid);
//PSID_IDENTIFIER_AUTHORITY GetSidIdentifierAuthority (PSID pSid);
//PDWORD GetSidSubAuthority (PSID pSid,DWORD nSubAuthority);
//PUCHAR GetSidSubAuthorityCount (PSID pSid);
//BOOL LookupAccountName (LPCSTR lpSystemName, LPCSTR lpAccountName, PSID Sid, LPDWORD cbSid,
//    LPSTR ReferencedDomainName, LPDWORD cbReferencedDomainName, PSID_NAME_USE peUse);
//BOOL LookupAccountSid (LPCSTR lpSystemName, PSID Sid, LPSTR Name, LPDWORD cbName,
//    LPSTR ReferencedDomainName, LPDWORD cbReferencedDomainName, PSID_NAME_USE peUse);
//BOOL GetTokenInformation (HANDLE TokenHandle, TOKEN_INFORMATION_CLASS TokenInformationClass,
//    LPVOID TokenInformation, DWORD TokenInformationLength, PDWORD ReturnLength);

DWORD FormatMessage(DWORD dwFlags, LPCVOID lpSource, DWORD dwMessageId, DWORD dwLanguageId,
 LPSTR lpBuffer, DWORD nSize, va_list *Arguments);

HANDLE GetCurrentThread(VOID);
DWORD GetCurrentThreadId(VOID);
HANDLE GetCurrentProcess(VOID);
DWORD GetCurrentProcessId(VOID);
BOOL GetComputerName (LPSTR lpBuffer, LPDWORD nSize);
BOOL CloseHandle(HANDLE hObject);
int GetWindowText(HWND hWnd, LPTSTR lpString, int nMaxCount ); 

//void InitializeCriticalSection (LPCRITICAL_SECTION);
//void DeleteCriticalSection (LPCRITICAL_SECTION);
//VOID EnterCriticalSection(LPCRITICAL_SECTION lpCriticalSection);
//VOID LeaveCriticalSection(LPCRITICAL_SECTION lpCriticalSection);
#define InitializeCriticalSection(LPCRITICAL_SECTION) ((void)0)
#define DeleteCriticalSection(LPCRITICAL_SECTION) ((void)0)
#define EnterCriticalSection(LPCRITICAL_SECTION) ((void)0)
#define LeaveCriticalSection(LPCRITICAL_SECTION) ((void)0)

BOOL GetComputerName (LPSTR lpBuffer, LPDWORD nSize);
//VOID Sleep(DWORD dwMilliseconds);
#define Sleep(M) sleep(M/1000)

BOOL LogonUser (LPSTR lpszUsername, LPSTR lpszDomain, LPSTR lpszPassword,
    DWORD dwLogonType, DWORD dwLogonProvider, PHANDLE phToken);


// missing function prototypes???
#define DebugBreak() DEBUG()
int GetLastError();
void SetLastError(int);
#ifndef unixcli
long GetProcAddress();
#endif
//UINT GetACP(void);
#define GetACP()	1033

// Stuff for MessageBox from WINUSER.H
int MessageBox(HWND hWnd , LPCSTR lpText, LPCSTR lpCaption, UINT uType);
/*
 * MessageBox() Flags
 */
#define MB_OK                       0x00000000L
#define MB_OKCANCEL                 0x00000001L
#define MB_ABORTRETRYIGNORE         0x00000002L
#define MB_YESNOCANCEL              0x00000003L
#define MB_YESNO                    0x00000004L
#define MB_RETRYCANCEL              0x00000005L
#define MB_ICONHAND                 0x00000010L
#define MB_ICONQUESTION             0x00000020L
#define MB_ICONEXCLAMATION          0x00000030L
#define MB_ICONASTERISK             0x00000040L

#ifndef unixcli
LocalFree(LPTSTR);
#endif

//Redefine timeb.h
#define _timeb			timeb
#define _ftime			ftime

//strcasecmp is defined in tdmXdev\d45\include\strings.h
#define _stricmp		strcasecmp
#define stricmp			strcasecmp
#define strnicmp		strncasecmp
#define _strnicmp		strncasecmp
#define _fcvt			fcvt
#define _ui64toa		_i64toa

#define WINAPI

#ifndef unixcli
#define Sleep(x)		sleep((x))
#endif

#define itoa			_itoa
#define ltoa			_ltoa
#define strupr			_strupr

char * _itoa(int, char *, int);
char *	_ltoa(long, char *, int);
char * _strupr(char *);
char* trim(char *string);
char *_strdup( const char *strSource );
#define strdup _strdup


// change the NT limit to NSK limit
#define _I64_MAX	LLONG_MAX

//============== NSK Driver Conversion ============================

#define FULL_SYSTEM_LEN 25
#define FULL_VOL_LEN 25
#define FULL_SUBVOL_LEN 25
#define EXT_FILENAME_LEN 120
#define	MAX_IMMU_MSG_LEN 120
#define PRODUCT_NO_SIZE 8
#define MAX_ERROR_TEXT_LEN 512

#define ODBC_DRIVER		"NonStop ODBC/MX"
#define DSNFILE			"MXODSN"
#define SYSTEM_PATH		"$SYSTEM.SYSTEM"

#define SYSTEM_DSNFILE	"$SYSTEM.SYSTEM.MXODSN"
#define USER_DSNFILE	DSNFILE

enum FILE_STATUS { FILE_CLOSED, FILE_OPENED, FILE_ERROR };

char* getUserFilePath(char* idsnFileName);

/*class OdbcDsn {
public:
	OdbcDsn();
	~OdbcDsn();
	BOOL WritePrivateProfileString(
		  LPCTSTR lpAppName,  // section name
		  LPCTSTR lpKeyName,  // key name
		  LPCTSTR lpString,   // string to add
		  LPCTSTR lpFileName  // initialization file
	);
	DWORD GetPrivateProfileString(
		  LPCTSTR lpAppName,        // section name
		  LPCTSTR lpKeyName,        // key name
		  LPCTSTR lpDefault,        // default string
		  LPTSTR lpReturnedString,  // destination buffer
		  DWORD nSize,              // size of destination buffer
		  LPCTSTR lpFileName        // initialization file name
	);
private:
	void	openFile(char* fileName);
	void	closeFile();
	short	readFile();
	BOOL	isFileOpen();
private:
	// global variables for the class
	FILE*	fp;
	char	dsnFileBuffer[EXT_FILENAME_LEN+1];
};*/

__int64 _atoi64( const char *string );
char *_i64toa( __int64 value, char *string, int radix );
char * _ui64toa( __int64 value, char *string, int radix );
char* _ultoa(unsigned long n, char *buff, int base);
//char *fcvt(double value,int count,int *dec,int *sign );

int _vsnprintf( char *buffer, size_t count, const char *format, va_list argptr );

HANDLE CreateEvent(LPSECURITY_ATTRIBUTES lpEventAttributes, BOOL bManualReset,BOOL bInitialState,LPTSTR lpName ); 
BOOL SetEvent(HANDLE hEvent );
DWORD WaitForMultipleObjects(DWORD nCount, const HANDLE *lpHandles, BOOL fWaitAll,DWORD dwMilliseconds );
DWORD FormatMessage (DWORD dwFlags, LPCVOID lpSource,DWORD dwMessageId,DWORD dwLanguageId,LPTSTR lpBuffer,DWORD nSize, va_list *Arguments);
int GetDateFormat(LCID Locale, DWORD dwFlags, CONST SYSTEMTIME *lpDate, LPCTSTR lpFormat, LPTSTR lpDateStr,int cchDate ); 
int GetTimeFormat(LCID Locale, DWORD dwFlags, const SYSTEMTIME *lpTime, LPCTSTR lpFormat, LPTSTR lpTimeStr, int cchTime ); 
int GetNumberFormat(LCID Locale, DWORD dwFlags, LPCTSTR lpValue, const NUMBERFMT *lpFormat, LPTSTR lpNumberStr, int cchNumber );
FARPROC GetProcAddress(HMODULE hModule,LPCWSTR lpProcName); 
HMODULE GetModuleHandle(LPCTSTR lpModuleName );
HLOCAL LocalFree(HLOCAL hMem );
void ODBCNLS_GetCodePage(unsigned long *dwACP);
void ODBCNLS_ValidateLanguage (unsigned long *dwLanguageId);

extern BOOL WriteMyPrivateProfileString(
  LPCTSTR lpAppName,  // section name
  LPCTSTR lpKeyName,  // key name
  LPCTSTR lpString,   // string to add
  LPCTSTR lpFileName  // initialization file
);

extern DWORD GetMyPrivateProfileString(
  LPCTSTR lpAppName,        // section name
  LPCTSTR lpKeyName,        // key name
  LPCTSTR lpDefault,        // default string
  LPTSTR lpReturnedString,  // destination buffer
  DWORD nSize,              // size of destination buffer
  LPCTSTR lpFileName        // initialization file name
);

#ifdef __cplusplus
}                                    /* End of extern "C" { */
#endif  /* __cplusplus */

#endif



