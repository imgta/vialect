from config import APP_DIR
import base64


IMG_DIR = APP_DIR / "imgs"
BTN_CLEAR_PATH = IMG_DIR / "clear-coffee.png"
BTN_PURP_PATH = IMG_DIR / "purp-coffee.png"

def img_base64(img_path: str) -> str:
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

BTN_NORMAL = img_base64(BTN_CLEAR_PATH)
BTN_HOVER = img_base64(BTN_PURP_PATH)

def tip_button():
    return f"""
    <div class="tip-container">
        <a href="https://www.buymeacoffee.com/imgta" target="_blank">
            <img src="data:image/png;base64,{BTN_NORMAL}" class="normal-image">
            <img src="data:image/png;base64,{BTN_HOVER}" class="hover-image">
        </a>
    </div>
    """

def via_header():
    return f"""
    <div class="heading-con">
    <p class="home-header">V<p><div class="header-i">|</div><p class="home-header">ALect</p>
    <span class="header-motto">Traverse digital oceans, <br> for treasures unseen.</span></div>
    </div>
    <hr>
    """

def icon_btns():
    return f"""
    <div class="tab-con">
    <div class="tabs">
    <!-- TAB 1 -->
    <a href="https://github.com/imgta" target="_blank">
        <label for="tab-01">
            <svg>
                <use xlink:href="#icon-01" class="icon" />
                <use xlink:href="#icon-01" class="icon-border" />
                <use xlink:href="#icon-01-fill" class="icon-fill" />
            </svg>
        </label>
    </a>
    <!-- TAB 2 -->
    <a href="https://www.linkedin.com/in/gordonta/" target="_blank">
        <label for="tab-02">
            <svg>
                <use xlink:href="#icon-02" class="icon" />
                <use xlink:href="#icon-02" class="icon-border" />
                <use xlink:href="#icon-02-fill" class="icon-fill" />
            </svg>
        </label>
    </a>
    </div>
    </div>

    <!-- GITHUB -->
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
    <symbol xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 512 512" id="icon-01">
        <path fill="#C9CBD5" d="M400 32H48C21.5 32 0 53.5 0 80v352c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V80c0-26.5-21.5-48-48-48zM277.3 415.7c-8.4 1.5-11.5-3.7-11.5-8 0-5.4.2-33 .2-55.3 0-15.6-5.2-25.5-11.3-30.7 37-4.1 76-9.2 76-73.1 0-18.2-6.5-27.3-17.1-39 1.7-4.3 7.4-22-1.7-45-13.9-4.3-45.7 17.9-45.7 17.9-13.2-3.7-27.5-5.6-41.6-5.6-14.1 0-28.4 1.9-41.6 5.6 0 0-31.8-22.2-45.7-17.9-9.1 22.9-3.5 40.6-1.7 45-10.6 11.7-15.6 20.8-15.6 39 0 63.6 37.3 69 74.3 73.1-4.8 4.3-9.1 11.7-10.6 22.3-9.5 4.3-33.8 11.7-48.3-13.9-9.1-15.8-25.5-17.1-25.5-17.1-16.2-.2-1.1 10.2-1.1 10.2 10.8 5 18.4 24.2 18.4 24.2 9.7 29.7 56.1 19.7 56.1 19.7 0 13.9.2 36.5.2 40.6 0 4.3-3 9.5-11.5 8-66-22.1-112.2-84.9-112.2-158.3 0-91.8 70.2-161.5 162-161.5S388 165.6 388 257.4c.1 73.4-44.7 136.3-110.7 158.3zm-98.1-61.1c-1.9.4-3.7-.4-3.9-1.7-.2-1.5 1.1-2.8 3-3.2 1.9-.2 3.7.6 3.9 1.9.3 1.3-1 2.6-3 3zm-9.5-.9c0 1.3-1.5 2.4-3.5 2.4-2.2.2-3.7-.9-3.7-2.4 0-1.3 1.5-2.4 3.5-2.4 1.9-.2 3.7.9 3.7 2.4zm-13.7-1.1c-.4 1.3-2.4 1.9-4.1 1.3-1.9-.4-3.2-1.9-2.8-3.2.4-1.3 2.4-1.9 4.1-1.5 2 .6 3.3 2.1 2.8 3.4zm-12.3-5.4c-.9 1.1-2.8.9-4.3-.6-1.5-1.3-1.9-3.2-.9-4.1.9-1.1 2.8-.9 4.3.6 1.3 1.3 1.8 3.3.9 4.1zm-9.1-9.1c-.9.6-2.6 0-3.7-1.5s-1.1-3.2 0-3.9c1.1-.9 2.8-.2 3.7 1.3 1.1 1.5 1.1 3.3 0 4.1zm-6.5-9.7c-.9.9-2.4.4-3.5-.6-1.1-1.3-1.3-2.8-.4-3.5.9-.9 2.4-.4 3.5.6 1.1 1.3 1.3 2.8.4 3.5zm-6.7-7.4c-.4.9-1.7 1.1-2.8.4-1.3-.6-1.9-1.7-1.5-2.6.4-.6 1.5-.9 2.8-.4 1.3.7 1.9 1.8 1.5 2.6z"/>
    </symbol>
    <symbol xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 512 512" id="icon-01-fill">
        <rect y="5%" x="-3%" rx="12.5%" ry="12.5%" width="92%" height="93%" fill="#4E29F0"/>
        <circle cx="50%" cy="50%" r="37%" width="75%" height="75%" fill="white"/>
        <path fill="#4E29F0" d="M400 32H48C21.5 32 0 53.5 0 80v352c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V80c0-26.5-21.5-48-48-48zM277.3 415.7c-8.4 1.5-11.5-3.7-11.5-8 0-5.4.2-33 .2-55.3 0-15.6-5.2-25.5-11.3-30.7 37-4.1 76-9.2 76-73.1 0-18.2-6.5-27.3-17.1-39 1.7-4.3 7.4-22-1.7-45-13.9-4.3-45.7 17.9-45.7 17.9-13.2-3.7-27.5-5.6-41.6-5.6-14.1 0-28.4 1.9-41.6 5.6 0 0-31.8-22.2-45.7-17.9-9.1 22.9-3.5 40.6-1.7 45-10.6 11.7-15.6 20.8-15.6 39 0 63.6 37.3 69 74.3 73.1-4.8 4.3-9.1 11.7-10.6 22.3-9.5 4.3-33.8 11.7-48.3-13.9-9.1-15.8-25.5-17.1-25.5-17.1-16.2-.2-1.1 10.2-1.1 10.2 10.8 5 18.4 24.2 18.4 24.2 9.7 29.7 56.1 19.7 56.1 19.7 0 13.9.2 36.5.2 40.6 0 4.3-3 9.5-11.5 8-66-22.1-112.2-84.9-112.2-158.3 0-91.8 70.2-161.5 162-161.5S388 165.6 388 257.4c.1 73.4-44.7 136.3-110.7 158.3zm-98.1-61.1c-1.9.4-3.7-.4-3.9-1.7-.2-1.5 1.1-2.8 3-3.2 1.9-.2 3.7.6 3.9 1.9.3 1.3-1 2.6-3 3zm-9.5-.9c0 1.3-1.5 2.4-3.5 2.4-2.2.2-3.7-.9-3.7-2.4 0-1.3 1.5-2.4 3.5-2.4 1.9-.2 3.7.9 3.7 2.4zm-13.7-1.1c-.4 1.3-2.4 1.9-4.1 1.3-1.9-.4-3.2-1.9-2.8-3.2.4-1.3 2.4-1.9 4.1-1.5 2 .6 3.3 2.1 2.8 3.4zm-12.3-5.4c-.9 1.1-2.8.9-4.3-.6-1.5-1.3-1.9-3.2-.9-4.1.9-1.1 2.8-.9 4.3.6 1.3 1.3 1.8 3.3.9 4.1zm-9.1-9.1c-.9.6-2.6 0-3.7-1.5s-1.1-3.2 0-3.9c1.1-.9 2.8-.2 3.7 1.3 1.1 1.5 1.1 3.3 0 4.1zm-6.5-9.7c-.9.9-2.4.4-3.5-.6-1.1-1.3-1.3-2.8-.4-3.5.9-.9 2.4-.4 3.5.6 1.1 1.3 1.3 2.8.4 3.5zm-6.7-7.4c-.4.9-1.7 1.1-2.8.4-1.3-.6-1.9-1.7-1.5-2.6.4-.6 1.5-.9 2.8-.4 1.3.7 1.9 1.8 1.5 2.6z"/>
    </symbol>

    <!-- LINKEDIN -->
    <symbol xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 512 512" width="36" height="36" id="icon-02">
        <g><path fill="C9CBD5" d="M273,233.8v-0.7c-0.1,0.2-0.3,0.5-0.5,0.7H273z"/><path fill="C9CBD5" d="M447.7,29.6H64.2C45.9,29.6,31,44.1,31,62v388c0,17.9,14.9,32.4,33.2,32.4h383.5c18.4,0,33.3-14.5,33.3-32.4   V62C481,44.1,466.1,29.6,447.7,29.6z M167.4,408.7h-68V204.2h68V408.7z M133.4,176.2H133c-22.8,0-37.5-15.7-37.5-35.3   c0-20.1,15.2-35.3,38.4-35.3c23.3,0,37.6,15.3,38,35.3C171.9,160.5,157.1,176.2,133.4,176.2z M412.5,408.7h-68V299.2   c0-27.5-9.8-46.2-34.4-46.2c-18.8,0-30,12.6-34.9,24.9c-1.8,4.4-2.2,10.5-2.2,16.6v114.2h-68c0,0,0.9-185.3,0-204.5h68v28.9   c9-13.9,25.2-33.8,61.3-33.8c44.7,0,78.2,29.2,78.2,92.1V408.7z"/></g>
    </symbol>
    <symbol xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="36" height="36" id="icon-02-fill">
        <g><rect x="50" y="50" width="75%" height="75%" fill="white"/><path fill="#4E29F0" d="M273,233.8v-0.7c-0.1,0.2-0.3,0.5-0.5,0.7H273z"/><path fill="#4E29F0" d="M447.7,29.6H64.2C45.9,29.6,31,44.1,31,62v388c0,17.9,14.9,32.4,33.2,32.4h383.5c18.4,0,33.3-14.5,33.3-32.4   V62C481,44.1,466.1,29.6,447.7,29.6z M167.4,408.7h-68V204.2h68V408.7z M133.4,176.2H133c-22.8,0-37.5-15.7-37.5-35.3   c0-20.1,15.2-35.3,38.4-35.3c23.3,0,37.6,15.3,38,35.3C171.9,160.5,157.1,176.2,133.4,176.2z M412.5,408.7h-68V299.2   c0-27.5-9.8-46.2-34.4-46.2c-18.8,0-30,12.6-34.9,24.9c-1.8,4.4-2.2,10.5-2.2,16.6v114.2h-68c0,0,0.9-185.3,0-204.5h68v28.9   c9-13.9,25.2-33.8,61.3-33.8c44.7,0,78.2,29.2,78.2,92.1V408.7z"/></g>
    </symbol>
    </svg>
    """