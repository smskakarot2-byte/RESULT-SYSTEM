import type { QueryKey, UseMutationOptions, UseMutationResult, UseQueryOptions, UseQueryResult } from "@tanstack/react-query";
import type { AnalyticsOverview, AuthUserEnvelope, BeginBrowserLoginParams, Course, CreateDepartmentBody, CreateUserBody, Department, DepartmentStat, DownloadTranscriptParams, GetCoursesParams, GetStudentResultsParams, GetToppersParams, HandleBrowserLoginCallbackParams, HealthStatus, MyProfile, StudentLookupResult, StudentResult, SystemUser, Topper, UploadAwardSheetBody, UploadResult } from "./api.schemas";
import { customFetch } from "../custom-fetch";
import type { ErrorType, BodyType } from "../custom-fetch";
type AwaitedInput<T> = PromiseLike<T> | T;
type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;
type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];
/**
 * @summary Health check
 */
export declare const getHealthCheckUrl: () => string;
export declare const healthCheck: (options?: RequestInit) => Promise<HealthStatus>;
export declare const getHealthCheckQueryKey: () => readonly ["/api/healthz"];
export declare const getHealthCheckQueryOptions: <TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData> & {
    queryKey: QueryKey;
};
export type HealthCheckQueryResult = NonNullable<Awaited<ReturnType<typeof healthCheck>>>;
export type HealthCheckQueryError = ErrorType<unknown>;
/**
 * @summary Health check
 */
export declare function useHealthCheck<TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Get the currently authenticated user
 */
export declare const getGetCurrentAuthUserUrl: () => string;
export declare const getCurrentAuthUser: (options?: RequestInit) => Promise<AuthUserEnvelope>;
export declare const getGetCurrentAuthUserQueryKey: () => readonly ["/api/auth/user"];
export declare const getGetCurrentAuthUserQueryOptions: <TData = Awaited<ReturnType<typeof getCurrentAuthUser>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCurrentAuthUser>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getCurrentAuthUser>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetCurrentAuthUserQueryResult = NonNullable<Awaited<ReturnType<typeof getCurrentAuthUser>>>;
export type GetCurrentAuthUserQueryError = ErrorType<unknown>;
/**
 * @summary Get the currently authenticated user
 */
export declare function useGetCurrentAuthUser<TData = Awaited<ReturnType<typeof getCurrentAuthUser>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCurrentAuthUser>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Start the browser OIDC login flow
 */
export declare const getBeginBrowserLoginUrl: (params?: BeginBrowserLoginParams) => string;
export declare const beginBrowserLogin: (params?: BeginBrowserLoginParams, options?: RequestInit) => Promise<unknown>;
export declare const getBeginBrowserLoginQueryKey: (params?: BeginBrowserLoginParams) => readonly ["/api/login", ...BeginBrowserLoginParams[]];
export declare const getBeginBrowserLoginQueryOptions: <TData = Awaited<ReturnType<typeof beginBrowserLogin>>, TError = ErrorType<void>>(params?: BeginBrowserLoginParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof beginBrowserLogin>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof beginBrowserLogin>>, TError, TData> & {
    queryKey: QueryKey;
};
export type BeginBrowserLoginQueryResult = NonNullable<Awaited<ReturnType<typeof beginBrowserLogin>>>;
export type BeginBrowserLoginQueryError = ErrorType<void>;
/**
 * @summary Start the browser OIDC login flow
 */
export declare function useBeginBrowserLogin<TData = Awaited<ReturnType<typeof beginBrowserLogin>>, TError = ErrorType<void>>(params?: BeginBrowserLoginParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof beginBrowserLogin>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Complete the browser OIDC login flow
 */
export declare const getHandleBrowserLoginCallbackUrl: (params?: HandleBrowserLoginCallbackParams) => string;
export declare const handleBrowserLoginCallback: (params?: HandleBrowserLoginCallbackParams, options?: RequestInit) => Promise<unknown>;
export declare const getHandleBrowserLoginCallbackQueryKey: (params?: HandleBrowserLoginCallbackParams) => readonly ["/api/callback", ...HandleBrowserLoginCallbackParams[]];
export declare const getHandleBrowserLoginCallbackQueryOptions: <TData = Awaited<ReturnType<typeof handleBrowserLoginCallback>>, TError = ErrorType<void>>(params?: HandleBrowserLoginCallbackParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof handleBrowserLoginCallback>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof handleBrowserLoginCallback>>, TError, TData> & {
    queryKey: QueryKey;
};
export type HandleBrowserLoginCallbackQueryResult = NonNullable<Awaited<ReturnType<typeof handleBrowserLoginCallback>>>;
export type HandleBrowserLoginCallbackQueryError = ErrorType<void>;
/**
 * @summary Complete the browser OIDC login flow
 */
export declare function useHandleBrowserLoginCallback<TData = Awaited<ReturnType<typeof handleBrowserLoginCallback>>, TError = ErrorType<void>>(params?: HandleBrowserLoginCallbackParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof handleBrowserLoginCallback>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Clear the session and begin OIDC logout
 */
export declare const getLogoutBrowserSessionUrl: () => string;
export declare const logoutBrowserSession: (options?: RequestInit) => Promise<unknown>;
export declare const getLogoutBrowserSessionQueryKey: () => readonly ["/api/logout"];
export declare const getLogoutBrowserSessionQueryOptions: <TData = Awaited<ReturnType<typeof logoutBrowserSession>>, TError = ErrorType<void>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof logoutBrowserSession>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof logoutBrowserSession>>, TError, TData> & {
    queryKey: QueryKey;
};
export type LogoutBrowserSessionQueryResult = NonNullable<Awaited<ReturnType<typeof logoutBrowserSession>>>;
export type LogoutBrowserSessionQueryError = ErrorType<void>;
/**
 * @summary Clear the session and begin OIDC logout
 */
export declare function useLogoutBrowserSession<TData = Awaited<ReturnType<typeof logoutBrowserSession>>, TError = ErrorType<void>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof logoutBrowserSession>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary List all departments
 */
export declare const getGetDepartmentsUrl: () => string;
export declare const getDepartments: (options?: RequestInit) => Promise<Department[]>;
export declare const getGetDepartmentsQueryKey: () => readonly ["/api/departments"];
export declare const getGetDepartmentsQueryOptions: <TData = Awaited<ReturnType<typeof getDepartments>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDepartments>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getDepartments>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetDepartmentsQueryResult = NonNullable<Awaited<ReturnType<typeof getDepartments>>>;
export type GetDepartmentsQueryError = ErrorType<unknown>;
/**
 * @summary List all departments
 */
export declare function useGetDepartments<TData = Awaited<ReturnType<typeof getDepartments>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDepartments>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Create a new department (admin only)
 */
export declare const getCreateDepartmentUrl: () => string;
export declare const createDepartment: (createDepartmentBody: CreateDepartmentBody, options?: RequestInit) => Promise<Department>;
export declare const getCreateDepartmentMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createDepartment>>, TError, {
        data: BodyType<CreateDepartmentBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createDepartment>>, TError, {
    data: BodyType<CreateDepartmentBody>;
}, TContext>;
export type CreateDepartmentMutationResult = NonNullable<Awaited<ReturnType<typeof createDepartment>>>;
export type CreateDepartmentMutationBody = BodyType<CreateDepartmentBody>;
export type CreateDepartmentMutationError = ErrorType<unknown>;
/**
 * @summary Create a new department (admin only)
 */
export declare const useCreateDepartment: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createDepartment>>, TError, {
        data: BodyType<CreateDepartmentBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createDepartment>>, TError, {
    data: BodyType<CreateDepartmentBody>;
}, TContext>;
/**
 * @summary Rename a department (admin only)
 */
export declare const getUpdateDepartmentUrl: (id: number) => string;
export declare const updateDepartment: (id: number, createDepartmentBody: CreateDepartmentBody, options?: RequestInit) => Promise<Department>;
export declare const getUpdateDepartmentMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof updateDepartment>>, TError, {
        id: number;
        data: BodyType<CreateDepartmentBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof updateDepartment>>, TError, {
    id: number;
    data: BodyType<CreateDepartmentBody>;
}, TContext>;
export type UpdateDepartmentMutationResult = NonNullable<Awaited<ReturnType<typeof updateDepartment>>>;
export type UpdateDepartmentMutationBody = BodyType<CreateDepartmentBody>;
export type UpdateDepartmentMutationError = ErrorType<unknown>;
/**
 * @summary Rename a department (admin only)
 */
export declare const useUpdateDepartment: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof updateDepartment>>, TError, {
        id: number;
        data: BodyType<CreateDepartmentBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof updateDepartment>>, TError, {
    id: number;
    data: BodyType<CreateDepartmentBody>;
}, TContext>;
/**
 * @summary Delete a department (admin only)
 */
export declare const getDeleteDepartmentUrl: (id: number) => string;
export declare const deleteDepartment: (id: number, options?: RequestInit) => Promise<void>;
export declare const getDeleteDepartmentMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteDepartment>>, TError, {
        id: number;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof deleteDepartment>>, TError, {
    id: number;
}, TContext>;
export type DeleteDepartmentMutationResult = NonNullable<Awaited<ReturnType<typeof deleteDepartment>>>;
export type DeleteDepartmentMutationError = ErrorType<unknown>;
/**
 * @summary Delete a department (admin only)
 */
export declare const useDeleteDepartment: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteDepartment>>, TError, {
        id: number;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof deleteDepartment>>, TError, {
    id: number;
}, TContext>;
/**
 * @summary List all system users (admin only)
 */
export declare const getGetUsersUrl: () => string;
export declare const getUsers: (options?: RequestInit) => Promise<SystemUser[]>;
export declare const getGetUsersQueryKey: () => readonly ["/api/users"];
export declare const getGetUsersQueryOptions: <TData = Awaited<ReturnType<typeof getUsers>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getUsers>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getUsers>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetUsersQueryResult = NonNullable<Awaited<ReturnType<typeof getUsers>>>;
export type GetUsersQueryError = ErrorType<unknown>;
/**
 * @summary List all system users (admin only)
 */
export declare function useGetUsers<TData = Awaited<ReturnType<typeof getUsers>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getUsers>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Create a professor account (admin only)
 */
export declare const getCreateSystemUserUrl: () => string;
export declare const createSystemUser: (createUserBody: CreateUserBody, options?: RequestInit) => Promise<SystemUser>;
export declare const getCreateSystemUserMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createSystemUser>>, TError, {
        data: BodyType<CreateUserBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createSystemUser>>, TError, {
    data: BodyType<CreateUserBody>;
}, TContext>;
export type CreateSystemUserMutationResult = NonNullable<Awaited<ReturnType<typeof createSystemUser>>>;
export type CreateSystemUserMutationBody = BodyType<CreateUserBody>;
export type CreateSystemUserMutationError = ErrorType<unknown>;
/**
 * @summary Create a professor account (admin only)
 */
export declare const useCreateSystemUser: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createSystemUser>>, TError, {
        data: BodyType<CreateUserBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createSystemUser>>, TError, {
    data: BodyType<CreateUserBody>;
}, TContext>;
/**
 * @summary Delete a user (admin only)
 */
export declare const getDeleteSystemUserUrl: (id: number) => string;
export declare const deleteSystemUser: (id: number, options?: RequestInit) => Promise<void>;
export declare const getDeleteSystemUserMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteSystemUser>>, TError, {
        id: number;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof deleteSystemUser>>, TError, {
    id: number;
}, TContext>;
export type DeleteSystemUserMutationResult = NonNullable<Awaited<ReturnType<typeof deleteSystemUser>>>;
export type DeleteSystemUserMutationError = ErrorType<unknown>;
/**
 * @summary Delete a user (admin only)
 */
export declare const useDeleteSystemUser: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteSystemUser>>, TError, {
        id: number;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof deleteSystemUser>>, TError, {
    id: number;
}, TContext>;
/**
 * @summary Get my GCUF profile (role, department)
 */
export declare const getGetMyProfileUrl: () => string;
export declare const getMyProfile: (options?: RequestInit) => Promise<MyProfile>;
export declare const getGetMyProfileQueryKey: () => readonly ["/api/users/me/profile"];
export declare const getGetMyProfileQueryOptions: <TData = Awaited<ReturnType<typeof getMyProfile>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMyProfile>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getMyProfile>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetMyProfileQueryResult = NonNullable<Awaited<ReturnType<typeof getMyProfile>>>;
export type GetMyProfileQueryError = ErrorType<unknown>;
/**
 * @summary Get my GCUF profile (role, department)
 */
export declare function useGetMyProfile<TData = Awaited<ReturnType<typeof getMyProfile>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMyProfile>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary List courses (filtered by department for professors)
 */
export declare const getGetCoursesUrl: (params?: GetCoursesParams) => string;
export declare const getCourses: (params?: GetCoursesParams, options?: RequestInit) => Promise<Course[]>;
export declare const getGetCoursesQueryKey: (params?: GetCoursesParams) => readonly ["/api/courses", ...GetCoursesParams[]];
export declare const getGetCoursesQueryOptions: <TData = Awaited<ReturnType<typeof getCourses>>, TError = ErrorType<unknown>>(params?: GetCoursesParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCourses>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getCourses>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetCoursesQueryResult = NonNullable<Awaited<ReturnType<typeof getCourses>>>;
export type GetCoursesQueryError = ErrorType<unknown>;
/**
 * @summary List courses (filtered by department for professors)
 */
export declare function useGetCourses<TData = Awaited<ReturnType<typeof getCourses>>, TError = ErrorType<unknown>>(params?: GetCoursesParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCourses>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Get a course by ID
 */
export declare const getGetCourseUrl: (id: number) => string;
export declare const getCourse: (id: number, options?: RequestInit) => Promise<Course>;
export declare const getGetCourseQueryKey: (id: number) => readonly [`/api/courses/${number}`];
export declare const getGetCourseQueryOptions: <TData = Awaited<ReturnType<typeof getCourse>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCourse>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getCourse>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetCourseQueryResult = NonNullable<Awaited<ReturnType<typeof getCourse>>>;
export type GetCourseQueryError = ErrorType<unknown>;
/**
 * @summary Get a course by ID
 */
export declare function useGetCourse<TData = Awaited<ReturnType<typeof getCourse>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCourse>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Delete a course and its results
 */
export declare const getDeleteCourseUrl: (id: number) => string;
export declare const deleteCourse: (id: number, options?: RequestInit) => Promise<void>;
export declare const getDeleteCourseMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteCourse>>, TError, {
        id: number;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof deleteCourse>>, TError, {
    id: number;
}, TContext>;
export type DeleteCourseMutationResult = NonNullable<Awaited<ReturnType<typeof deleteCourse>>>;
export type DeleteCourseMutationError = ErrorType<unknown>;
/**
 * @summary Delete a course and its results
 */
export declare const useDeleteCourse: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteCourse>>, TError, {
        id: number;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof deleteCourse>>, TError, {
    id: number;
}, TContext>;
/**
 * @summary Upload and parse a GCUF Award Sheet PDF
 */
export declare const getUploadAwardSheetUrl: () => string;
export declare const uploadAwardSheet: (uploadAwardSheetBody: UploadAwardSheetBody, options?: RequestInit) => Promise<UploadResult>;
export declare const getUploadAwardSheetMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof uploadAwardSheet>>, TError, {
        data: BodyType<UploadAwardSheetBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof uploadAwardSheet>>, TError, {
    data: BodyType<UploadAwardSheetBody>;
}, TContext>;
export type UploadAwardSheetMutationResult = NonNullable<Awaited<ReturnType<typeof uploadAwardSheet>>>;
export type UploadAwardSheetMutationBody = BodyType<UploadAwardSheetBody>;
export type UploadAwardSheetMutationError = ErrorType<unknown>;
/**
 * @summary Upload and parse a GCUF Award Sheet PDF
 */
export declare const useUploadAwardSheet: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof uploadAwardSheet>>, TError, {
        data: BodyType<UploadAwardSheetBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof uploadAwardSheet>>, TError, {
    data: BodyType<UploadAwardSheetBody>;
}, TContext>;
/**
 * @summary Get all student results for a course
 */
export declare const getGetCourseResultsUrl: (courseId: number) => string;
export declare const getCourseResults: (courseId: number, options?: RequestInit) => Promise<StudentResult[]>;
export declare const getGetCourseResultsQueryKey: (courseId: number) => readonly [`/api/results/course/${number}`];
export declare const getGetCourseResultsQueryOptions: <TData = Awaited<ReturnType<typeof getCourseResults>>, TError = ErrorType<unknown>>(courseId: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCourseResults>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getCourseResults>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetCourseResultsQueryResult = NonNullable<Awaited<ReturnType<typeof getCourseResults>>>;
export type GetCourseResultsQueryError = ErrorType<unknown>;
/**
 * @summary Get all student results for a course
 */
export declare function useGetCourseResults<TData = Awaited<ReturnType<typeof getCourseResults>>, TError = ErrorType<unknown>>(courseId: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getCourseResults>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Lookup results by roll number and session
 */
export declare const getGetStudentResultsUrl: (params: GetStudentResultsParams) => string;
export declare const getStudentResults: (params: GetStudentResultsParams, options?: RequestInit) => Promise<StudentLookupResult>;
export declare const getGetStudentResultsQueryKey: (params?: GetStudentResultsParams) => readonly ["/api/results/student", ...GetStudentResultsParams[]];
export declare const getGetStudentResultsQueryOptions: <TData = Awaited<ReturnType<typeof getStudentResults>>, TError = ErrorType<unknown>>(params: GetStudentResultsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getStudentResults>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getStudentResults>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetStudentResultsQueryResult = NonNullable<Awaited<ReturnType<typeof getStudentResults>>>;
export type GetStudentResultsQueryError = ErrorType<unknown>;
/**
 * @summary Lookup results by roll number and session
 */
export declare function useGetStudentResults<TData = Awaited<ReturnType<typeof getStudentResults>>, TError = ErrorType<unknown>>(params: GetStudentResultsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getStudentResults>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Download PDF transcript for a student
 */
export declare const getDownloadTranscriptUrl: (rollNo: string, params?: DownloadTranscriptParams) => string;
export declare const downloadTranscript: (rollNo: string, params?: DownloadTranscriptParams, options?: RequestInit) => Promise<Blob>;
export declare const getDownloadTranscriptQueryKey: (rollNo: string, params?: DownloadTranscriptParams) => readonly [`/api/results/transcript/${string}`, ...DownloadTranscriptParams[]];
export declare const getDownloadTranscriptQueryOptions: <TData = Awaited<ReturnType<typeof downloadTranscript>>, TError = ErrorType<unknown>>(rollNo: string, params?: DownloadTranscriptParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof downloadTranscript>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof downloadTranscript>>, TError, TData> & {
    queryKey: QueryKey;
};
export type DownloadTranscriptQueryResult = NonNullable<Awaited<ReturnType<typeof downloadTranscript>>>;
export type DownloadTranscriptQueryError = ErrorType<unknown>;
/**
 * @summary Download PDF transcript for a student
 */
export declare function useDownloadTranscript<TData = Awaited<ReturnType<typeof downloadTranscript>>, TError = ErrorType<unknown>>(rollNo: string, params?: DownloadTranscriptParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof downloadTranscript>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Global dashboard stats
 */
export declare const getGetAnalyticsOverviewUrl: () => string;
export declare const getAnalyticsOverview: (options?: RequestInit) => Promise<AnalyticsOverview>;
export declare const getGetAnalyticsOverviewQueryKey: () => readonly ["/api/analytics/overview"];
export declare const getGetAnalyticsOverviewQueryOptions: <TData = Awaited<ReturnType<typeof getAnalyticsOverview>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getAnalyticsOverview>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getAnalyticsOverview>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetAnalyticsOverviewQueryResult = NonNullable<Awaited<ReturnType<typeof getAnalyticsOverview>>>;
export type GetAnalyticsOverviewQueryError = ErrorType<unknown>;
/**
 * @summary Global dashboard stats
 */
export declare function useGetAnalyticsOverview<TData = Awaited<ReturnType<typeof getAnalyticsOverview>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getAnalyticsOverview>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Per-department average scores and student counts
 */
export declare const getGetDepartmentAnalyticsUrl: () => string;
export declare const getDepartmentAnalytics: (options?: RequestInit) => Promise<DepartmentStat[]>;
export declare const getGetDepartmentAnalyticsQueryKey: () => readonly ["/api/analytics/departments"];
export declare const getGetDepartmentAnalyticsQueryOptions: <TData = Awaited<ReturnType<typeof getDepartmentAnalytics>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDepartmentAnalytics>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getDepartmentAnalytics>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetDepartmentAnalyticsQueryResult = NonNullable<Awaited<ReturnType<typeof getDepartmentAnalytics>>>;
export type GetDepartmentAnalyticsQueryError = ErrorType<unknown>;
/**
 * @summary Per-department average scores and student counts
 */
export declare function useGetDepartmentAnalytics<TData = Awaited<ReturnType<typeof getDepartmentAnalytics>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDepartmentAnalytics>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Session and department toppers ranked by percentage
 */
export declare const getGetToppersUrl: (params?: GetToppersParams) => string;
export declare const getToppers: (params?: GetToppersParams, options?: RequestInit) => Promise<Topper[]>;
export declare const getGetToppersQueryKey: (params?: GetToppersParams) => readonly ["/api/analytics/toppers", ...GetToppersParams[]];
export declare const getGetToppersQueryOptions: <TData = Awaited<ReturnType<typeof getToppers>>, TError = ErrorType<unknown>>(params?: GetToppersParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getToppers>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getToppers>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetToppersQueryResult = NonNullable<Awaited<ReturnType<typeof getToppers>>>;
export type GetToppersQueryError = ErrorType<unknown>;
/**
 * @summary Session and department toppers ranked by percentage
 */
export declare function useGetToppers<TData = Awaited<ReturnType<typeof getToppers>>, TError = ErrorType<unknown>>(params?: GetToppersParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getToppers>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Get all unique sessions in the system
 */
export declare const getGetSessionsUrl: () => string;
export declare const getSessions: (options?: RequestInit) => Promise<string[]>;
export declare const getGetSessionsQueryKey: () => readonly ["/api/analytics/sessions"];
export declare const getGetSessionsQueryOptions: <TData = Awaited<ReturnType<typeof getSessions>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getSessions>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getSessions>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetSessionsQueryResult = NonNullable<Awaited<ReturnType<typeof getSessions>>>;
export type GetSessionsQueryError = ErrorType<unknown>;
/**
 * @summary Get all unique sessions in the system
 */
export declare function useGetSessions<TData = Awaited<ReturnType<typeof getSessions>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getSessions>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export {};
//# sourceMappingURL=api.d.ts.map