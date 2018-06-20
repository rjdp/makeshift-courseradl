import os
import requests
import time
import sys

video_quality = '720p'

one_of_specialization_course_id = "pNXe13ICEeeBKg4MjLYj6A" #"BIU_pgCCEeiZdg6RDGBSdg" #"7H35pMSrEeefQQqXI6t6yg" #"pNXe13ICEeeBKg4MjLYj6A" #"ARf5_jvZEeeYEBLbuVGJ2g" #"nA4RUW01EeW8nRIpKnwp7Q" #get id of any course within a specializarion, this course id is from google IT Support Professional Certificate Specialization

spec_url = "https://www.coursera.org/api/onDemandSpecializations.v1?fields=courseIds,interchangeableCourseIds,launchedAt,logo,memberships,metadata,partnerIds,premiumExperienceVariant,onDemandSpecializationMemberships.v1(suggestedSessionSchedule),onDemandSpecializationSuggestedSchedule.v1(suggestedSessions),partners.v1(homeLink,name),courses.v1(courseProgress,description,membershipIds,startDate,v2Details,vcMembershipIds),v2Details.v1(onDemandSessions,plannedLaunchDate),memberships.v1(grade,vcMembershipId),vcMemberships.v1(certificateCodeWithGrade)&includes=courseIds,memberships,partnerIds,onDemandSpecializationMemberships.v1(suggestedSessionSchedule),courses.v1(courseProgress,membershipIds,v2Details,vcMembershipIds),v2Details.v1(onDemandSessions)&q=primary&courseId={}".format(one_of_specialization_course_id)

courses =  list(map(lambda x: {'name': x['name'], 'slug':x['slug'], 'id':x['id']},requests.get(spec_url).json().get('linked').get('courses.v1')))

course_url = "https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={}&includes=modules%2Clessons%2CpassableItemGroups%2CpassableItemGroupChoices%2CpassableLessonElements%2Citems%2Ctracks%2CgradePolicy&fields=moduleIds%2ConDemandCourseMaterialModules.v1(name%2Cslug%2Cdescription%2CtimeCommitment%2ClessonIds%2Coptional%2ClearningObjectives)%2ConDemandCourseMaterialLessons.v1(name%2Cslug%2CtimeCommitment%2CelementIds%2Coptional%2CtrackId)%2ConDemandCourseMaterialPassableItemGroups.v1(requiredPassedCount%2CpassableItemGroupChoiceIds%2CtrackId)%2ConDemandCourseMaterialPassableItemGroupChoices.v1(name%2Cdescription%2CitemIds)%2ConDemandCourseMaterialPassableLessonElements.v1(gradingWeight%2CisRequiredForPassing)%2ConDemandCourseMaterialItems.v2(name%2Cslug%2CtimeCommitment%2CcontentSummary%2CisLocked%2ClockableByItem%2CitemLockedReasonCode%2CtrackId%2ClockedStatus%2CitemLockSummary)%2ConDemandCourseMaterialTracks.v1(passablesCount)&showLockedItems=true"

lecture_url = "https://www.coursera.org/api/onDemandLectureVideos.v1/{}~{}?includes=video&fields=onDemandVideos.v1(sources%2Csubtitles%2CsubtitlesVtt%2CsubtitlesTxt)"

is_specialization =  True 


if not is_specialization:
    course_id = "7H35pMSrEeefQQqXI6t6yg"
    courses = [{'slug': "ibm-blockchain-essentials-for-developers", 'id':course_id, 'name':'IBM Blockchain Foundation for Developers'}]

def download_file(file_name, file_url):
    print(file_url)
    start = time.clock()
    r = requests.get(file_url, stream = True)
    total_length = r.headers.get('content-length')
    dl = 0
    with open(file_name.strip().replace("/", " ") ,"wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                dl += len(chunk)
                file.write(chunk)
                done = int(50 * dl / int(total_length))
                sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))

for course in courses:
    url = course_url.format(course['slug'])
    if not os.path.exists(course['name']):
        os.makedirs(course['name'])
    os.chdir(course['name'])
    print("Downloading course = {} {} {}".format('$'*5, course['name'], '$'*5))
    lectures = [item for item in requests.get(url).json().get('linked').get('onDemandCourseMaterialItems.v2') if item.get('contentSummary').get('typeName') == 'lecture']
    for i, lecture in enumerate(lectures):
        file_name =  str(i) + ' - '+lecture['name'] + '.mp4'
        if not os.path.exists(file_name.strip().replace("/", " ")):
            print("Downloading lecture = {} {} {}".format('%'*5, lecture['name'], '%'*5))
            lec_url = lecture_url.format(course.get('id'), lecture['id'])
            lec_video_url = requests.get(lec_url).json().get('linked').get('onDemandVideos.v1')[0].get('sources').get('byResolution').get(video_quality).get('mp4VideoUrl')
            download_file(file_name, lec_video_url)
    os.chdir('..')