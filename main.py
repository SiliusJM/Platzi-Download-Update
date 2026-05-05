# Import the required modules
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import subprocess as _subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import requests, re
import time
import multiprocessing
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os
from pyfiglet import Figlet

# callprocess
from process import callProcess
from utils import (
    createFolder,
    create_env_file,
    remove_word_from_file,
    print_progress_bar,
    checkFolderExists,
    checkFileExists,
    colorize_text,
    checkIfffmpegInstalled,
    is_folder_empty,
)
from customRequest import request_with_random_user_agent


# region Variables and selectors
webdriver_path = "C:/chromedriver.exe"
emailSelector = "email"
continueBtnSelector = "continueBtn"
pwdSelector = "password"
submitLoginBtnSelector = '//*[@id="login-v2"]/div/div/div/div[3]/form/button'

checkCaptchaSelector = "MainLayout"
checkVideoSelector = "VideoPlayer"
checkLectureSelector = "styles_Lecture"
checkQuizSelector = "StartQuizOverview"
contentSelector = "styles_IFrame"
checkExamSelector = "StartExamOverview"

publishedDateSelector = "//*[contains(@class, 'MaterialHeading-published')]"
courseInfoLinkSelector = "MaterialDesktopHeading-course"
courseInfoSelector = "Hero-base"
promorBannerSelector = "PromoBanner-content"
courseNameSelector = "BadgeWithText_BadgeWithText"
videoDivSelector = "video-js"
resourceBtnSelector = "resources_tab"
checkAvailableResourcesSelector = "Archivos de la clase"

skipQuizBtnSelector = "StartQuizOverview-btn--skip"
classNameSelector = '//*[@data-qa="class_title"]'
classNumberSelector = "MaterialHeading-tag"
nextClassBtnSelector = '//*[@data-qa="next_class_button"]'

checkDownloadableResourcesSelector = "FilesTree-download"
checkDownloadableFileSelector = "fa-download"
checkDownloadAllSelector = "FilesTree_FilesTree__Download"

selectorErrorMsgs = {
    checkCaptchaSelector: "An error has occurred while validating the captcha.",
    checkVideoSelector: "There was an error finding the video",
    checkLectureSelector: "There was an error finding the lecture",
    checkQuizSelector: "There was an error finding the quiz",
    courseNameSelector: "There was an error finding the course name",
    videoDivSelector: "There was an error finding the video",
    skipQuizBtnSelector: "There was an error finding the skip quiz button",
    classNameSelector: "There was an error finding the class name",
    nextClassBtnSelector: "There was an error finding the next class button",
    checkDownloadableResourcesSelector: "There was an error finding the downloadable resources",
    checkDownloadableFileSelector: "There was an error finding the downloadable file",
}
# endregion


def downloadResources(driver, courseName, nameClass):
    # find the resource button
    # checkResourceBtn = driver.find_elements(
    #     By.CSS_SELECTOR, f"[data-qa='{resourceBtnSelector}']"
    # )
    # if not checkResourceBtn:
    #     return
    # checkResourceBtn = checkResourceBtn[0]
    # checkResourceBtn.click()
    try:
        downloadAllBtn = driver.find_elements(
            By.XPATH, f"//*[contains(@class, '{checkDownloadAllSelector}')]"
        )
        path = f"./videos/{courseName}/{nameClass}/resources/"
        # get the href of the download links
        if downloadAllBtn:
            downloadAllBtn = downloadAllBtn[0]
            os.makedirs(path, exist_ok=True)
            link = downloadAllBtn.get_attribute("href")
            # get the download file name
            fileName = f"{nameClass}.zip"
            # download the file
            if link != "":
                if not checkFileExists(
                    f"\\videos\\{courseName}\\{nameClass}\\resources\\{fileName}"
                ):
                    response = requests.get(link)
                    if response.status_code == 200:
                        with open(f"{path}{fileName}", "wb") as f:
                            f.write(response.content)
        else:
            # get the download elements by href
            download_elements = driver.find_elements(
                By.XPATH,
                "//a[contains(@href, 'https://static.platzi.com/media/public/uploads')]",
            )
            os.makedirs(path, exist_ok=True)
            for element in download_elements:
                # Check if has download attribute
                if not element.get_attribute("download"):
                    continue
                link = element.get_attribute("href")
                # get the file name
                fileName = f"{nameClass.split('.')[0]}. {element.text}"
                # download the file
                if link != "":
                    if not checkFileExists(
                        f"\\videos\\{courseName}\\{nameClass}\\resources\\{fileName}"
                    ):
                        response = request_with_random_user_agent(link)
                        if response.status_code == 200:
                            with open(f"{path}{fileName}", "wb") as f:
                                f.write(response.content)
        if is_folder_empty(path):
            os.rmdir(path)
        return
    except:
        downloadAllBtn = None

    try:
        checkAvailableResources = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//*[contains(text(), '{checkAvailableResourcesSelector}')]",
                )
            )
        )
    except:
        checkAvailableResources = None
    if checkAvailableResources:
        download_elements = driver.find_elements(By.CSS_SELECTOR, "a[download]")
        if download_elements:
            if not checkFolderExists(f"\\videos\\{courseName}\\{nameClass}\\resources"):
                createFolder("\\videos\\" + courseName + "\\" + nameClass + "\\resources")
            # get the href of the download links
            for element in download_elements:
                link = element.get_attribute("href")
                # get the file name
                fileName = f"{nameClass.split('.')[0]}. {element.text}"
                # download the file
                if link != "":
                    if not checkFileExists(
                        f"\\videos\\{courseName}\\{nameClass}\\resources\\{fileName}"
                    ):
                        response = requests.get(link)
                        if response.status_code == 200:
                            path = "./videos/{}/{}/resources/".format(courseName, nameClass)
                            with open(f"{path}{fileName}", "wb") as f:
                                f.write(response.content)


def menu():
    titleFont = Figlet(font="larry3d")

    # Print colored text
    print(colorize_text(titleFont.renderText("  Platzi Download")))
    print(colorize_text("By OscarDogar\n", "4;32"))
    print(colorize_text("Updated by SiliusXix(JMSG)\n", "4;32"))

    while True:
        # The input string containing the URL
        startUrl = input("Please enter the URL of the class you want to download: ")
        # Accept old format (/clases/) and new format (/cursos/course/class/)
        if "clases" in startUrl or ("cursos" in startUrl and startUrl.count("/") >= 6):
            break
        print(colorize_text("Please enter a specific class URL (not the course page).\nExample: https://platzi.com/cursos/nombre-curso/nombre-clase/", 31))
    print("")
    inputOption = input(
        "Do you want to download only this video or this and the following videos?\n\n1. Just this one\n2. This one and the following\nType: "
    )
    while inputOption != "1" and inputOption != "2":
        inputOption = input(
            "Do you want to download only this video or this and the following videos?\n\n1. Just this one\n2. This one and the following\nType: "
        )

    return inputOption, startUrl


def main():
    if not checkIfffmpegInstalled():
        print("Please install ffmpeg")
        input("Press enter to exit")
        return
    create_env_file()
    work()


def getClassName(driver):
    classNameElements = driver.find_elements(By.XPATH, classNameSelector)
    if len(classNameElements) > 1:
        className = classNameElements[1]
    elif len(classNameElements) == 1:
        className = classNameElements[0]
    else:
        return "clase_sin_nombre"
    result = re.sub(r"Clase\s\d.*$", "", className.text)
    return re.sub(r"[^\w\s]", "", result)


def getClassNumber(driver):
    html_content = driver.page_source
    # Try original selector
    position = html_content.find(classNumberSelector)
    if position != -1:
        rest_of_text = html_content[position + len(classNumberSelector) :]
        numbersPattern = r"\d+\s*/\s*\d+"
        match = re.search(numbersPattern, rest_of_text)
        if match:
            number = match.group().split("/")
            return [substring.strip() for substring in number]
    # Fallback: try data-qa class_title for number pattern
    numbersPattern = r'(\d+)\s*de\s*(\d+)'
    match = re.search(numbersPattern, html_content)
    if match:
        return [match.group(1), match.group(2)]
    # Last fallback: return unknown
    print("Class number was not found, using fallback.")
    return ["1", "1"]


def nextPage(driver):
    # Dismiss any open modal overlay (e.g. profile completion popup)
    try:
        skip_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Omitir por ahora')]")
        skip_btn.click()
        time.sleep(1)
    except Exception:
        pass
    # Also dismiss via modal overlay close button if present
    try:
        overlay = driver.find_element(By.ID, "modal-overlay")
        if overlay.is_displayed():
            driver.execute_script("arguments[0].style.pointerEvents='none';", overlay)
    except Exception:
        pass

    btnNextList = driver.find_elements(By.XPATH, nextClassBtnSelector)
    if not btnNextList:
        print("There was an error finding the next class button")
        return False
    btnNext = btnNextList[0]

    # check if the button is disabled
    if btnNext.is_enabled():
        try:
            btnNext.click()
        except Exception:
            # Modal still intercepting — use JS click to bypass
            driver.execute_script("arguments[0].click();", btnNext)
    else:
        print("There was an error finding the next class button")
        return False
    return True


def format_entry(name, url):
    return f"#EXTINF:-1,{name}\n{url}"


def _extract_json_object(text, key):
    """Extract a JSON object value for a given key from text using brace counting."""
    marker = f'"{key}":{{'
    pos = text.find(marker)
    if pos == -1:
        return None
    start = pos + len(f'"{key}":')
    depth = 0
    in_string = False
    escape_next = False
    for i, ch in enumerate(text[start:]):
        if escape_next:
            escape_next = False
            continue
        if ch == '\\' and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                json_str = text[start:start + i + 1]
                try:
                    return json.loads(json_str)
                except Exception:
                    return None
    return None


def getVideoAndSubInfo(driver):
    video_info = None
    subs_info = None
    driver.refresh()
    time.sleep(2)

    def find_scripts():
        els = driver.find_elements(By.XPATH, '//script[contains(text(), "serverC")]')
        if els:
            return els
        return driver.find_elements(By.XPATH, '//script[contains(text(), "mdstrm")]')

    elements = find_scripts()
    if len(elements) == 0:
        for _ in range(3):
            driver.refresh()
            time.sleep(2)
            elements = find_scripts()
            if elements:
                break

    for element in elements:
        script_content = driver.execute_script("return arguments[0].textContent;", element)
        cleaned = script_content.replace("\\", "")

        # Old structure: serverC.hls
        if video_info is None:
            serverC = _extract_json_object(cleaned, "serverC")
            if serverC and "hls" in serverC:
                video_info = {"serverC": serverC}

        # New structure: dash URL (Platzi 2024+)
        if video_info is None:
            dashMatch = re.search(r'"dash":"(https://mdstrm\.com/video/[^"]+\.mpd)"', cleaned)
            if dashMatch:
                dash_url = dashMatch.group(1)
                video_id = dash_url.split('/video/')[1].replace('.mpd', '')
                # Build serverC-compatible structure so rest of code works unchanged
                hls_url = f"https://mdstrm.com/video/{video_id}.m3u8"
                video_info = {"serverC": {"hls": hls_url}}

        # Subtitles (movin) - same in both old and new structure
        if subs_info is None:
            movin = _extract_json_object(cleaned, "movin")
            if movin and "subtitles" in movin:
                subs_info = {"movin": movin}

        if video_info and subs_info:
            break

    # If subtitles not found yet, search any script containing "movin" (some classes store it separately)
    if subs_info is None:
        movin_scripts = driver.find_elements(By.XPATH, '//script[contains(text(), "movin")]')
        for el in movin_scripts:
            content = driver.execute_script("return arguments[0].textContent;", el)
            cleaned = content.replace("\\", "")
            movin = _extract_json_object(cleaned, "movin")
            if movin and "subtitles" in movin and movin["subtitles"]:
                subs_info = {"movin": movin}
                break

    return video_info, subs_info


def getCourseImage(driver, link, courseName, published):
    driver.get(link)
    time.sleep(0.5)
    try:
        # Check if the element is present
        banner = driver.find_element(By.CLASS_NAME, promorBannerSelector)
        driver.execute_script(
            "arguments[0].parentNode.removeChild(arguments[0]);", banner
        )
    except NoSuchElementException:
        pass
    try:
        # save the course link
        with open(f"./videos/{courseName}/Course Link.txt", "w", encoding="utf-8") as f:
            f.write(link + "\n" + published)
        courseInfo = driver.find_element(By.CLASS_NAME, courseInfoSelector)
        driver.execute_script("arguments[0].scrollIntoView();", courseInfo)

        # Wait for a moment to ensure the element is fully visible
        driver.implicitly_wait(5)

        # Get the location and size of the element
        location = courseInfo.location
        size = courseInfo.size
        filePath = f"videos/{courseName}/folder.png"
        # Take a screenshot of the element
        driver.save_screenshot(filePath)

        # Open the screenshot using PIL
        img = Image.open(filePath)

        # Calculate the coordinates for cropping
        left = location["x"]
        top = location["y"]
        right = left + size["width"] + 529
        bottom = top + size["height"] + 74.8

        # Crop and save the screenshot of the element
        img = img.crop((left, top, right, bottom))
        img.save(filePath)
        # this is to change the folder icon because only show the last thumbnail in the folder
        current_file_name = filePath
        new_file_name = filePath[:-3] + "jpg"
        os.rename(current_file_name, new_file_name)
    except:
        print("There was an error getting the course image")
        pass


def getClassPositionFromSidebar(driver, startUrl):
    """
    Open the 'Ver clases' modal to detect the current class position and total count.
    Returns (current_pos, total_classes). Falls back to (1, 0) on failure.
    """
    try:
        course_slug = startUrl.rstrip("/").split("/")[-2]
        current_slug = startUrl.rstrip("/").split("/")[-1]

        # Click "Ver clases" button to open the class list modal
        ver_btn = driver.find_elements(By.XPATH, '//*[normalize-space(text())="Ver clases"]')
        if ver_btn:
            ver_btn[0].click()
            time.sleep(1)

        # Collect all class links for this course (href contains /course_slug/)
        class_links = driver.find_elements(
            By.XPATH, f'//a[contains(@href, "/{course_slug}/")]'
        )

        # Deduplicate by slug, preserving DOM order
        seen_slugs = set()
        unique_slugs = []
        for el in class_links:
            href = el.get_attribute("href") or ""
            slug = href.rstrip("/").split("/")[-1]
            if slug and slug != course_slug and slug not in seen_slugs:
                seen_slugs.add(slug)
                unique_slugs.append(slug)

        total = len(unique_slugs)
        pos = 1
        if current_slug in unique_slugs:
            pos = unique_slugs.index(current_slug) + 1

        # Close the modal
        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except Exception:
            pass

        return pos, total
    except Exception:
        return 1, 0


def work():
    try:
        inputOption, startUrl = menu()
        start_time = time.time()
        createFolder("\\videos")
        videosUrl = {}
        subtitles = {}
        lecturesUrls = []
        words_to_remove = os.environ.get("WORDS_TO_REMOVE")
        # Create the webdriver object and pass the arguments
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        # Ignores any certificate errors if there is any
        chrome_options.add_argument("--ignore-certificate-errors")
        # Chrome will start in Headless mode
        # chrome_options.add_argument('headless')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        # Detect installed Chrome major version to download matching ChromeDriver
        def get_chrome_major_version():
            try:
                result = _subprocess.run(
                    ['reg', 'query', r'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon', '/v', 'version'],
                    capture_output=True, text=True
                )
                match = re.search(r'(\d+)\.\d+\.\d+\.\d+', result.stdout)
                if match:
                    return int(match.group(1))
            except Exception:
                pass
            return None
        chrome_version = get_chrome_major_version()
        driver = uc.Chrome(
            options=chrome_options,
            version_main=chrome_version,
        )
        driver.get("https://platzi.com/login/")
        load_dotenv()
        time.sleep(0.5)
        emailInput = driver.find_element(By.ID, emailSelector)
        emailInput.send_keys(os.environ.get("EMAIL"))
        time.sleep(0.5)
        continueBtn = driver.find_element(
            By.CSS_SELECTOR, f"[data-qa='{continueBtnSelector}']"
        )
        # check if the button is disabled
        if continueBtn.is_enabled():
            continueBtn.click()
        else:
            print("There was an error finding the continue button")

        # Wait for password field (may take longer if captcha appears first)
        pwdInput = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    pwdSelector,
                )
            )
        )
        pwdInput.send_keys(os.environ.get("PWD"))
        time.sleep(0.5)
        continueBtn = driver.find_element(
            By.CSS_SELECTOR, f"[data-qa='{continueBtnSelector}']"
        )
        # check if the button is disabled
        if continueBtn.is_enabled():
            continueBtn.click()
        else:
            print("There was an error finding the login button")

        # Wait for login to complete (may require solving captcha manually)
        print(colorize_text("Waiting for login... If a captcha appears, solve it manually in Chrome.", "4;33"))
        checkCaptcha = driver.find_elements(By.ID, checkCaptchaSelector)
        timeout_login = 120  # 2 minutes to solve captcha
        elapsed = 0
        while not checkCaptcha and elapsed < timeout_login:
            time.sleep(1)
            elapsed += 1
            checkCaptcha = driver.find_elements(By.ID, checkCaptchaSelector)
        if not checkCaptcha:
            print(colorize_text("Login timeout. Please try again.", 31))
            driver.close()
            return
        driver.get(startUrl)
        time.sleep(2)
        # Dismiss Platzi profile completion popup if it appears
        try:
            skip_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Omitir por ahora')]")
            skip_btn.click()
            time.sleep(1)
        except Exception:
            pass
        # Check the name of the video
        time.sleep(2)
        lecture = driver.find_elements(
            By.XPATH, f"//*[contains(@class, '{checkLectureSelector}')]"
        )
        quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
        content = driver.find_elements(
            By.XPATH, f"//*[contains(@class, '{contentSelector}')]"
        )
        try:
            published = driver.find_element(By.XPATH, publishedDateSelector).text
        except:
            published = ""
        # Get course name from page title (most reliable - title format: "Class | CourseName | Platzi")
        courseName = ""
        try:
            page_title = driver.title
            title_parts = page_title.split(" | ")
            if len(title_parts) >= 2:
                raw_name = title_parts[-2].strip()  # second-to-last part is always the course name
                courseName = re.sub(r"[^\w\s]", "", raw_name).strip()
        except Exception:
            pass
        # Fallback to CSS selector, then URL slug
        if not courseName:
            courseNameElements = driver.find_elements(
                By.XPATH, f"//*[contains(@class, '{courseNameSelector}')]"
            )
            if len(courseNameElements) > 1:
                courseName = re.sub(r"[^\w\s]", "", courseNameElements[1].text).strip()
            elif len(courseNameElements) == 1:
                courseName = re.sub(r"[^\w\s]", "", courseNameElements[0].text).strip()
            else:
                urlParts = startUrl.rstrip("/").split("/")
                courseName = urlParts[-2] if len(urlParts) >= 2 else "curso"
        if courseName:
            createFolder("\\videos\\{}".format(courseName))
            courseInfoLink = driver.find_elements(
                By.XPATH, f"//*[contains(@class, '{courseInfoLinkSelector}')]"
            )
            # get href of the course
            courseLink = courseInfoLink[0].get_attribute("href") if courseInfoLink else startUrl
            if not checkFileExists(
                f"\\videos\\{courseName}\\folder.png"
            ) and not checkFileExists(f"\\videos\\{courseName}\\folder.jpg"):
                getCourseImage(driver, courseLink, courseName, published)
                driver.get(startUrl)
        if len(quiz) == 0 and len(lecture) == 0 and len(content) == 0:
            videoPlayer = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, videoDivSelector))
            )
        else:
            videoPlayer = None
        print("Finding videos...")
        if not checkFileExists(f"\\videos\\{courseName}\\playlist.m3u"):
            with open(f"./videos/{courseName}/playlist.m3u", "w", encoding="utf-8") as file:
                file.write("#EXTM3U\n")
        nameClass = ""
        countVideoErrors = 0
        # Detect starting class position and total from sidebar (click "Ver clases")
        classCounter, totalClasses = getClassPositionFromSidebar(driver, startUrl)
        classCounter -= 1  # will be incremented when the first class is processed
        number = [str(max(classCounter, 1)), str(totalClasses)]
        while True:
            try:
                videoPlayer = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, videoDivSelector))
                )
            except:
                videoPlayer = None
            if not videoPlayer:
                try:
                    lecture = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                f"//*[contains(@class, '{checkLectureSelector}')]",
                            )
                        )
                    )
                except:
                    lecture = None
            if videoPlayer or lecture:
                classCounter += 1
                number = [str(classCounter), str(totalClasses)]
            if videoPlayer:
                video_info = None
                subs_info = None
                nameClass = getClassName(driver)
                nameClass = f"{number[0]}. {nameClass}"
                video_info, subs_info = getVideoAndSubInfo(driver)
                if video_info:
                    video = video_info["serverC"]["hls"]
                    # URL is already complete, no transformation needed
                    respVideo = requests.get(video)
                    # check the status code
                    if respVideo.status_code == 200:
                        videosUrl[nameClass] = video
                        with open(f"./videos/{courseName}/playlist.m3u", "a", encoding="utf-8") as file:
                            ##check if the video is already in the playlist
                            if (
                                not format_entry(nameClass, video)
                                in open(f"./videos/{courseName}/playlist.m3u", encoding="utf-8", errors="replace").read()
                            ):
                                file.write(format_entry(nameClass, video) + "\n")
                        video = ""
                    else:
                        countVideoErrors += 1
                        print(
                            colorize_text(
                                f"There was an error getting the video: {nameClass}", 31
                            )
                        )
                if subs_info:
                    subtitles[nameClass] = subs_info["movin"]["subtitles"]
                downloadResources(driver, courseName, nameClass)
            elif lecture != None:
                createFolder("\\videos\\" + courseName + "\\lectures")
                nameClass = getClassName(driver)
                nameClass = f"{number[0]}. {nameClass}"
                lecturesUrls.append(f"{number[0]}. {driver.current_url}")
                res = driver.execute_cdp_cmd("Page.captureSnapshot", {})
                # Write the file locally
                with open(
                    "./videos/{}/lectures/{}.mhtml".format(courseName, nameClass),
                    "w",
                    newline="",
                    encoding="utf-8",
                ) as f:
                    f.write(res["data"])
            else:
                quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
                if len(quiz) != 0:
                    jumpNext = driver.find_element(By.CLASS_NAME, skipQuizBtnSelector)
                    jumpNext.click()
                    popup = driver.find_elements(By.XPATH, f"//*[contains(@class, 'Button-module_Button--secondary_')]")
                    if popup:
                        popup[0].click()
                else:
                    content = driver.find_elements(
                        By.XPATH, f"//*[contains(@class, '{contentSelector}')]"
                    )
                    exam = driver.find_elements(By.CLASS_NAME, checkExamSelector)
                    # Also detect exam/evaluacion pages by URL (CSS class may have changed)
                    if len(exam) != 0 or "/evaluacion/" in driver.current_url:
                        break
            if inputOption == "2":
                print_progress_bar(int(number[0]), int(number[1]))
            if inputOption == "1":
                break
            elif len(quiz) == 0:
                if not nextPage(driver):
                    break
            elif (
                videoPlayer != None
                and lecture != None
                and len(quiz) != 0
                and len(content) != 0
            ):
                break
            videoPlayer = None
            lecture = None
            quiz = []
            content = []
            time.sleep(1)
        driver.close()
        if len(lecturesUrls) > 0:
            with open(f"./videos/{courseName}/lectures/Lectures Urls.txt", "a", encoding="utf-8") as f:
                for item in lecturesUrls:
                    f.write("%s\n" % item)
        if videosUrl or subtitles:
            callProcess(videosUrl, subtitles, courseName)
        if words_to_remove:
            # convert string to list and remove spaces
            words_to_remove = words_to_remove.split(",")
            words_to_remove = [x.strip() for x in words_to_remove]
            remove_word_from_file(f"./videos/{courseName}/lectures/", words_to_remove)
        print("--------Finished--------")
        if countVideoErrors > 0:
            print(
                colorize_text(
                    f"There were {countVideoErrors} errors getting the videos.", 31
                )
            )
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        print(
            f"The download took {hours} hours, {minutes} minutes, and {seconds} seconds to run."
        )
    except KeyboardInterrupt as e:
        print("The program was stopped")
    except Exception as e:
        # Regular expression pattern to match the selector
        pattern = r'"selector":"\.(.*?)"'
        # Find the match using the pattern
        match = re.search(pattern, str(e))
        if match:
            selector = match.group(1)
            if selector in selectorErrorMsgs:
                print(colorize_text(selectorErrorMsgs[selector], 31))
            else:
                print(colorize_text("There was an error finding the elements", 31))
        elif "target window already closed" in str(e):
            print(colorize_text("Chrome browser has been closed", 31))
        elif "no such element: Unable to locate element" in str(e):
            print("There was an error finding the elements")
        elif "Cannot determine loading status" in str(e):
            print("The page did not load completely")
        elif "stale element not found" in str(e):
            print(
                "It looks like the page has been refreshed and the element is no longer attached to the DOM"
            )
        elif "object has no attribute 'status_code'" in str(e):
            print("There was an error downloading the video")
        elif "Chrome failed to start'" in str(e):
            print("Chrome failed to start")
        elif "cannot access local variable 'video'" in str(e):
            print(
                "There was an error finding the video, it seems that the server is not available"
            )
        else:
            import traceback
            print(colorize_text("Unexpected error:", 31))
            traceback.print_exc()


if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()
    main()
    input("Press enter to exit")
