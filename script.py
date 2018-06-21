import os
import requests
import time
import sys

video_quality = '360p' # available qualities 360p, 540p, 720p

""" 
In order to get courseId go to a course page open network tab in browser dev tools and search for "onDemandSpecializations" 
in search input of network tab and then go to videos section of say week 1 , check the query param "courseId" its value is what we use can use as value for "one_of_specialization_course_id"
variable seen below incase the course belongs to a specialization other wise set is_specialization = False and course_id to the value of
courseId query_params's value

"""

one_of_specialization_course_id =  "iSxVEG07EeW3YxLB1q9I2w"#"pNXe13ICEeeBKg4MjLYj6A" #"BIU_pgCCEeiZdg6RDGBSdg" #"7H35pMSrEeefQQqXI6t6yg" #"pNXe13ICEeeBKg4MjLYj6A" #"ARf5_jvZEeeYEBLbuVGJ2g" #"nA4RUW01EeW8nRIpKnwp7Q" #get id of any course within a specializarion, this course id is from google IT Support Professional Certificate Specialization

spec_url = "https://www.coursera.org/api/onDemandSpecializations.v1?fields=courseIds,interchangeableCourseIds,launchedAt,logo,memberships,metadata,partnerIds,premiumExperienceVariant,onDemandSpecializationMemberships.v1(suggestedSessionSchedule),onDemandSpecializationSuggestedSchedule.v1(suggestedSessions),partners.v1(homeLink,name),courses.v1(courseProgress,description,membershipIds,startDate,v2Details,vcMembershipIds),v2Details.v1(onDemandSessions,plannedLaunchDate),memberships.v1(grade,vcMembershipId),vcMemberships.v1(certificateCodeWithGrade)&includes=courseIds,memberships,partnerIds,onDemandSpecializationMemberships.v1(suggestedSessionSchedule),courses.v1(courseProgress,membershipIds,v2Details,vcMembershipIds),v2Details.v1(onDemandSessions)&q=primary&courseId={}".format(one_of_specialization_course_id)

courses =  list(map(lambda x: {'name': x['name'], 'slug':x['slug'], 'id':x['id']},requests.get(spec_url).json().get('linked').get('courses.v1')))

course_url = "https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={}&includes=modules%2Clessons%2CpassableItemGroups%2CpassableItemGroupChoices%2CpassableLessonElements%2Citems%2Ctracks%2CgradePolicy&fields=moduleIds%2ConDemandCourseMaterialModules.v1(name%2Cslug%2Cdescription%2CtimeCommitment%2ClessonIds%2Coptional%2ClearningObjectives)%2ConDemandCourseMaterialLessons.v1(name%2Cslug%2CtimeCommitment%2CelementIds%2Coptional%2CtrackId)%2ConDemandCourseMaterialPassableItemGroups.v1(requiredPassedCount%2CpassableItemGroupChoiceIds%2CtrackId)%2ConDemandCourseMaterialPassableItemGroupChoices.v1(name%2Cdescription%2CitemIds)%2ConDemandCourseMaterialPassableLessonElements.v1(gradingWeight%2CisRequiredForPassing)%2ConDemandCourseMaterialItems.v2(name%2Cslug%2CtimeCommitment%2CcontentSummary%2CisLocked%2ClockableByItem%2CitemLockedReasonCode%2CtrackId%2ClockedStatus%2CitemLockSummary)%2ConDemandCourseMaterialTracks.v1(passablesCount)&showLockedItems=true"

courseid_url = "https://www.coursera.org/api/onDemandCourses.v1?q=slug&slug={}&includes=instructorIds%2CpartnerIds%2C_links&fields=brandingImage%2CcertificatePurchaseEnabledAt%2Cpartners.v1(squareLogo%2CrectangularLogo)%2Cinstructors.v1(fullName)%2CoverridePartnerLogos%2CsessionsEnabledAt%2CdomainTypes%2CpremiumExperienceVariant%2CisRestrictedMembership"

lecture_url = "https://www.coursera.org/api/onDemandLectureVideos.v1/{}~{}?includes=video&fields=onDemandVideos.v1(sources%2Csubtitles%2CsubtitlesVtt%2CsubtitlesTxt)"

is_specialization =  True 


if not is_specialization:
    course_id = "7H35pMSrEeefQQqXI6t6yg"  # plug in appropriate course id, slug, name  manually
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
    try:
        lectures = [item for item in requests.get(url).json().get('linked').get('onDemandCourseMaterialItems.v2') if item.get('contentSummary').get('typeName') == 'lecture']
        print("Downloading course = {} {} {}".format('$'*5, course['name'].replace(':', '-'), '$'*5))
        if not os.path.exists(course['name'].replace(':', '-')):
            os.makedirs(course['name'].replace(':', '-'))
        os.chdir(course['name'].replace(':', '-'))
        for i, lecture in enumerate(lectures):
            try:
                file_name =  str(i) + ' - '+lecture['name'] + '.mp4'
                if not os.path.exists(file_name.strip().replace("/", " ")):
                    print("Downloading lecture = {} {} {}".format('%'*5, lecture['name'], '%'*5))
                    courseid = requests.get(courseid_url.format(course['slug'])).json().get('elements')[0].get('id')
                    lec_url = lecture_url.format(courseid, lecture['id'])
                    lec_video_url = requests.get(lec_url).json().get('linked').get('onDemandVideos.v1')[0].get('sources').get('byResolution').get(video_quality).get('mp4VideoUrl')
                    download_file(file_name, lec_video_url)
            except:
                pass
        os.chdir('..')
    except:
        pass