##IFixThat this file contains contributions from
# -PR--https://github.com/ytdl-org/youtube-dl/pull/30689/files#diff-86cb77d6ab845290abde260b0edac01f2152551e7440f236972734e9d3c70510L1-R182
# -PR--https://github.com/ytdl-org/youtube-dl/pull/30774/files#diff-86cb77d6ab845290abde260b0edac01f2152551e7440f236972734e9d3c70510
# and myself

from __future__ import unicode_literals

import re
import itertools

from math import isinf

from .common import (
    InfoExtractor,
    SearchInfoExtractor,
)
from ..compat import (
    compat_kwargs,
    compat_str,
    compat_urlparse,
    compat_urllib_parse_unquote,
    compat_urllib_request,
)
##IFixThat clean up below imports
from ..utils import (
    clean_html,
    determine_ext,
    ExtractorError,
    int_or_none,
    parse_duration,
    str_to_int,
    urljoin,
    url_basename,
    compat_urlparse,
    remove_end,
    remove_start,
#    T,
#    traverse_obj,
#    try_call,
#    txt_or_none,
#    join_nonempty,
#    LazyList,
    merge_dicts,
    parse_count,
    get_element_by_class,
    get_element_by_id,
    get_elements_by_class,
    extract_attributes,
)

##IFixThat additional imports (I insert them into every Extractor that I modify - can be removed if not needed)

import datetime
import os

##IFixThat debug print_or_not

def _ifixthat_print_or_not(line):
    doprint = 1 # 0=normal , 1=debug
    if doprint > 0:
        print(' [[[ '+line)

##IFixThat general helper functions (I insert them into every Extractor that I modify - can be removed if not needed)

def _ifixthat_helper_file_exists(self,filename):
    _ifixthat_print_or_not('does '+filename+' exist?')
    if os.path.exists(filename):
        _ifixthat_print_or_not('yes')
        return True
    else:
        _ifixthat_print_or_not('no')
        return False

def _ifixthat_helper_check_strbytelen(self,string):
    strbytelen = len(string)
    # is string (filename/paths) too long -> this value is customized to my setup and works for me - probably needs some more testing with diff. filesystems, filepaths, videos, ...
    if strbytelen > 274:
        return False
    else:
        return True

def _ifixthat_helper_file_mv(self,filename_old, filename_new):
    if self._ifixthat_helper_check_strbytelen(filename_new):
        os.rename(filename_old, filename_new)

def _ifixthat_helper_file_archive(self,filename):
    self._ifixthat_helper_file_mv(filename, filename+'.backup_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def _ifixthat_helper_file_write(self,filename, content):
    if self._ifixthat_helper_file_exists(filename):
        #_ifixthat_print_or_not('backing up previous '+filename)
        self._ifixthat_helper_file_archive(filename)
    #_ifixthat_print_or_not('writing file')
    #check len of file
    if self._ifixthat_helper_check_strbytelen(filename):
        myfile = open(filename, "wt")
        myfile.write(content)
        myfile.close()

def _ifixthat_helper_file_read(self,filename):
    if self._ifixthat_helper_file_exists(filename):
        myfile = open(filename, "rt")
        myfilecontent = myfile.read()
        myfile.close()
        return myfilecontent
    else:
        return ''

##IFixThat_end

#################################################################################################################################################################################### single video

class XVideosIE(InfoExtractor):

    ## urls tested in firefox-browser

    # -> https://www.xvideos.com/video.ifbhcpf7201/when_girls_play_-_adriana_chechik_abella_danger_-_betrayal_-_twistys
    # https://www.xvideos.com/video50011247/when_girls_play_-_adriana_chechik_abella_danger_-_tradimento_-_twistys
    # https://www.xvideos.com/video.ifbhcpf7201/0
    # https://xvideos.com/video.ifbhcpf7201/0
    # https://www.xvideos.com/video50011247/0
    # https://xvideos.com/video50011247/0

    # -> https://www.xvideos.com/embedframe/ifbhcpf7201
    # https://flashservice.xvideos.com/embedframe/ifbhcpf7201

    # -> https://www.xvideos.com/embedframe/50011247
    # https://flashservice.xvideos.com/embedframe/50011247

    # -> https://www.xvideos.es/video.ifbhcpf7201/when_girls_play_-_adriana_chechik_abella_danger_-_betrayal_-_twistys
    # https://xvideos.es/video.ifbhcpf7201/when_girls_play_-_adriana_chechik_abella_danger_-_betrayal_-_twistys
    # https://www.xvideos.es/video.ifbhcpf7201/0
    # https://xvideos.es/video.ifbhcpf7201/0
    # https://www.xvideos.es/video50011247/0
    # https://xvideos.es/video50011247/0

    ##IFixThat TODO= old+new ID-scheme
    _VALID_URL = r'''(?x)
                    (?:
                        https?://
                            (?:
                                # xvideos\d+\.com redirects to xvideos.com
                                # (?P<country>[a-z]{2})\.xvideos.com too: catch it anyway
                                (?:[^/]+\.)?xvideos\.com/(?:video\.|prof-video-click/model/[^/]+/)|
                                (?:www\.)?xvideos\.es/video|
                                (?:www|flashservice)\.xvideos\.com/embedframe/|
                                static-hw\.xvideos\.com/swf/xv-player\.swf\?.*?\bid_video=
                            )|
                        xvideos:
                    )(?P<id>[a-z0-9]+)
                 '''
    #_VALID_URL = r'''(?x)
    #                (?:
    #                    https?://
    #                        (?:
    #                            # xvideos\d+\.com redirects to xvideos.com
    #                            # (?P<country>[a-z]{2})\.xvideos.com too: catch it anyway
    #                            (?:[^/]+\.)?xvideos\.com/(?:video|prof-video-click/model/[^/]+/)|
    #                            (?:www\.)?xvideos\.es/video|
    #                            (?:www|flashservice)\.xvideos\.com/embedframe/|
    #                            static-hw\.xvideos\.com/swf/xv-player\.swf\?.*?\bid_video=
    #                        )|
    #                    xvideos:
    #                )(?P<id>\d+)
    #             '''
    #_VALID_URL = r'''(?x)
    #                https?://
    #                    (?:
    #                        (?:[^/]+\.)?xvideos2?\.com/video\.|
    #                        (?:www\.)?xvideos\.es/video|
    #                        flashservice\.xvideos\.com/embedframe/|
    #                        static-hw\.xvideos\.com/swf/xv-player\.swf\?.*?\bid_video=
    #                    )
    #                    (?P<id>[a-z0-9]+)
    #                '''
    #_VALID_URL = r'''(?x)
    #                https?://
    #                    (?:
    #                        (?:[^/]+\.)?xvideos2?\.com/video|
    #                        (?:www\.)?xvideos\.es/video|
    #                        flashservice\.xvideos\.com/embedframe/|
    #                        static-hw\.xvideos\.com/swf/xv-player\.swf\?.*?\bid_video=
    #                    )
    #                    (?P<id>[0-9]+)
    #                '''

    ##IFixThat TODO ?)md5 1) other-urls
    _TESTS = [{
        'url': 'https://www.xvideos.com/video.ifbhcpf7201/when_girls_play_-_adriana_chechik_abella_danger_-_betrayal_-_twistys',
        'md5': '---', # how when nideo is hls
        'info_dict': {
            'id': 'ifbhcpf7201',
            'id_new': 'ifbhcpf7201',
            'id_old': '50011247',
            'ext': 'mp4',
            'title': 'When Girls Play - (Adriana Chechik, Abella Danger) - Betrayal - Twistys', # When Girls Play - &lpar;Adriana Chechik&comma; Abella Danger&rpar; - Betrayal - Twistys
            'duration': 720,
            'age_limit': 18,
        }
    }, {
        'url': 'x1',
        'only_matching': True,
    }, {
        'url': 'x2',
        'only_matching': True,
    }, {
        'url': 'x3',
        'only_matching': True
    }]

    # from dirkf pr
    #@classmethod
    #def suitable(cls, url):
    #    EXCLUDE_IE = (XVideosRelatedIE, )
    #    return (False if any(ie.suitable(url) for ie in EXCLUDE_IE)
    #            else super(XVideosIE, cls).suitable(url))

    def _real_extract(self, url):
        video_id = self._match_id(url)

        ##IFixThat update initial download to accommodate for old and new ID-scheme -- due to redirect always new ?

        ift_vidid_wp = '.'+video_id # assume new alphanum with .
        ift_vidid_new = video_id
        ift_vidid_old = '' # get from webpage later
        ift_idscheme = 'new'
        if video_id.isdigit():
            ift_vidid_wp = video_id # ok - old because numbers-only
            ift_vidid_old = video_id
            ift_vidid_new = '' # get from webpage later
            ift_idscheme = 'old'

        webpage = self._download_webpage(
            'https://www.xvideos.com/video%s/0' % ift_vidid_wp, video_id)

        ##IFixThat_end

        mobj = re.search(r'<h1 class="inlineError">(.+?)</h1>', webpage)
        if mobj:
            raise ExtractorError('%s said: %s' % (self.IE_NAME, clean_html(mobj.group(1))), expected=True)

        ##IFixThat old/new ids

        video_meta_matches = re.findall(
            r',"id_video":([0-9]+),"encoded_id_video":"([a-z0-9]+)",', webpage)
        if len(video_meta_matches) > 0:
            if ift_idscheme == 'new':
                ift_vidid_old = video_meta_matches[0][0]
            else:
                ift_vidid_new = video_meta_matches[0][1]

        ##IFixThat_end

        title = self._html_search_regex(
            (r'<title>(?P<title>.+?)\s+-\s+XVID',
             r'setVideoTitle\s*\(\s*(["\'])(?P<title>(?:(?!\1).)+)\1'),
            webpage, 'title', default=None,
            group='title') or self._og_search_title(webpage)

        thumbnails = []
        for preference, thumbnail in enumerate(('', '169')):
            thumbnail_url = self._search_regex(
                r'setThumbUrl%s\(\s*(["\'])(?P<thumbnail>(?:(?!\1).)+)\1' % thumbnail,
                webpage, 'thumbnail', default=None, group='thumbnail')
            if thumbnail_url:
                thumbnails.append({
                    'url': thumbnail_url,
                    'preference': preference,
                })

        duration = int_or_none(self._og_search_property(
            'duration', webpage, default=None)) or parse_duration(
            self._search_regex(
                ## original
                #r'<span[^>]+class=["\']duration["\'][^>]*>.*?(\d[^<]+)',
                ## dirkf pr
                r'''<span [^>]*\bclass\s*=\s*["']duration\b[^>]+>.*?(\d[^<]+)''',
                webpage, 'duration', fatal=False))

        formats = []

        ##IFixThat -- probably no loger needed - I have not encountered flv-videos for multiple years now
        video_url = compat_urllib_parse_unquote(self._search_regex(
            r'flv_url=(.+?)&', webpage, 'video URL', default=''))
        if video_url:
            formats.append({
                'url': video_url,
                'format_id': 'flv',
            })

        ##IFixThat_end

        video_url = re.findall(
            r'"contentUrl": "([^"]+)"', webpage)
        #_ifixthat_print_or_not('video_url')
        #_ifixthat_print_or_not(video_url)
        # should be only one
        if len(video_url) > 0:
            formats.append({
                'url': video_url[0],
                'format_id': 'contentUrl',
            })

        ##IFixThat_end

        for kind, _, format_url in re.findall(
                r'setVideo([^(]+)\((["\'])(http.+?)\2\)', webpage):
            format_id = kind.lower()
            if format_id == 'hls':
                ## orig/my
                #formats.extend(self._extract_m3u8_formats(
                #    format_url, video_id, 'mp4',
                #    entry_protocol='m3u8_native', m3u8_id='hls', fatal=False))
                ## dirkf pr
                hls_formats = self._extract_m3u8_formats(
                    format_url, video_id, 'mp4',
                    entry_protocol='m3u8_native', m3u8_id='hls', fatal=False)
                self._check_formats(hls_formats, video_id)
                formats.extend(hls_formats)
            elif format_id in ('urllow', 'urlhigh'):
                formats.append({
                    'url': format_url,
                    'format_id': '%s-%s' % (determine_ext(format_url, 'mp4'), format_id[3:]),
                    'quality': -2 if format_id.endswith('low') else None,
                })

        self._sort_formats(formats)

        ##IFixThat old/new ids ++ for later : uploader + tags + actors

## ,"id_video":50011247,"encoded_id_video":"ifbhcpf7201","uploader_id":11422220,"uploader":"twistys1","uploader_url":"\/twistys1","video_tags":["lesbian","teen","hardcore","latina","rough","squirt","big-ass","cheater","twistys","cheat","ass-play","when-girls-play"],"video_models":{"22053533":{"name":"Abella Danger","profile":"abella-danger","uri":"\/pornstars\/abella-danger"},"8415660":{"name":"Adriana Chechik","profile":"adriana-chechik","uri":"\/pornstars\/adriana-chechik"}}}};</script>

##,"id_video":35757155,"encoded_id_video":"iihvcpkf375","uploader_id":24819879,"uploader":"girlswayofficial","uploader_url":"\/girlswayofficial","video_tags":["lesbian","boobs","hot","pornstar","brunette","fingering","squirting","masturbation","pussy-licking","college","facesitting","tribbing","big-tits","nice-ass","romance","girl-on-girl","natural-tits","adriana-chechik","megan-rain"],"video_models":{"8415660":{"name":"Adriana Chechik","profile":"adriana-chechik","uri":"\/pornstars\/adriana-chechik"},"14193845":{"name":"Megan Rain","profile":"megan-rain","uri":"\/pornstars\/megan-rain"}}}};</script>

##,"id_video":1067228,"encoded_id_video":"htuldcb8a9","uploader_id":1705824,"uploader":"","video_tags":[],"video_models":{"6957567":{"name":"Leonie Saint","profile":"leonie-saint","uri":"\/models\/leonie-saint"}}}};</script>

##,"id_video":64065209,"encoded_id_video":"kdhlebvb94e","uploader_id":522199271,"uploader":"sperm-mania","uploader_url":"\/sperm-mania","video_tags":["facial","creampie","shorthair","bukkake","bbw","marie","cumshot-compilation","huge-cumshot","pussy-bukkake","cum-fetish","cum-in-panties","japanese-bukkake","cum-lube","cock-cum","bukkake-compilation"],"video_models":[]}};</script>

#### TO
#,"uploader_id":([0-9]+),"uploader":"([-a-z0-9]+|)",(?:,"uploader_url":"\\/([-a-z0-9]+)"|)
#,"video_tags":(\[[^]].\]),
#,"video_models":{"([0-9]+)":{"name":"Abella Danger","profile":"abella-danger","uri":"\/pornstars\/abella-danger"},?...}

        ##IFixThat adding uploader

        #@DarkFighterLuke
        #creator_data = re.findall(r'<a href="(?P<creator_url>.+?)" class="btn btn-default label main uploader-tag hover-name"><span class="name">(?P<creator>.+?)<', webpage)
        #creator = None
        #uploader_url = None
        #if creator_data != []:
        #    uploader_url, creator = creator_data[0][0:2]

        # get uploader from meta
        uploader = 'NULL'
        uploader_id = 'NULL'
        uploader_url = 'NULL'
        video_meta_matches = re.findall(
            r',"uploader_id":([0-9]+),"uploader":"([-a-z0-9]+|)",(?:,"uploader_url":"\\/([-a-z0-9]+)"|)', webpage)
        if len(video_meta_matches) > 0:
            uploader_id = video_meta_matches[0][0]
            if video_meta_matches[0][1] == '':
                # replace with _ as empty strings may not work in paths
                uploader = '_'
                uploader_url = '/'
            else:
                uploader = video_meta_matches[0][1]
                uploader_url = video_meta_matches[0][2]

        # get uploader from url-list for more info
        uploader_type = 'NULL'
        uploader_name_url = '_'
        uploader_name_txt = '_'
        uploader_name_txt_orig = '_'
        uploader_user_id = 'NULL'
        uploader_user_profile = 'NULL'
        # <li class="main-uploader"><a href="/channels/studio-fow" class="btn btn-default label main uploader-tag hover-name"><span class="name"><span class="icon-f icf-device-tv-v2"></span> Studio Fow</span><span class="user-subscribe" data-user-id="9267136" data-user-profile="studio-fow"><span class="count">308k</span></span></a></li>
        # <li class="main-uploader"><a href="/profiles/hmvthief" class="btn btn-default label main uploader-tag hover-name"><span class="name">Hmvthief</span><span class="user-subscribe" data-user-id="507454529" data-user-profile="hmvthief"><span class="count">2k</span></span></a></li>
        uploader_matches = re.findall(r'<li(?: class="main-uploader"|)><a href="/(amateur-channels|channels|model-channels|models|pornstar-channels|pornstars|profiles|)/?([a-zA-Z0-9\-\._]+)" class="btn btn-default label main uploader-tag hover-name"><span class="name">(?:<span class="icon-f icf-device-tv-v2"></span> |)([a-zA-Z0-9\-\._\s]+)</span>(?:<span class="icon-f icf-check-circle verified" title="Verified uploader"></span>|)<span class="[a-zA-Z0-9\-\s]*" data-user-id="([0-9]+)" data-user-profile="([a-zA-Z0-9\-\._]+)">', webpage)
        #print(uploader_matches)
        #print(len(uploader_matches))
        if len(uploader_matches) > 0:
            if not uploader_matches[0][0] == '':
                uploader_type = uploader_matches[0][0]
                _ifixthat_print_or_not('non empty type')
            else:
                uploader_type = 'channels' # empty ''=channels
                _ifixthat_print_or_not('empty type = channels')
            uploader_name_url = uploader_matches[0][1]
            uploader_name_txt_orig = uploader_matches[0][2]
            # replace " " with "-"
            uploader_name_txt = uploader_name_txt_orig.replace(" ","-")
            uploader_user_id = uploader_matches[0][3]
            uploader_user_profile = uploader_matches[0][4]

        ##IFixThat adding actors

        #@DarkFighterLuke
        #actors_data = re.findall(r'href="(?P<actor_url>/pornstars/.+?)" class="btn btn-default label profile hover-name"><span class="name">(?P<actor_name>.+?)</span>', webpage)
        #actors = []
        #if actors_data != []:
        #    for actor_tuple in actors_data:
        #        actors.append({
        #            'given_name': actor_tuple[1],
        #            'url': urljoin(url, actor_tuple[0]),
        #        })

        # get all others
        otherprofiles = []
        ## <li class="model"><a href="/pornstars/kendra-spade" class="btn btn-default label profile hover-name is-pornstar" data-id="194201359"><span class="name"><span class="icon-f icf-star-o"></span> Kendra Spade</span><span class="user-subscribe" data-user-id="194201359" data-user-profile="kendra-spade"><span class="count">283k</span></span></a></li>
        # <li class="model"><a href="/models/leonie-saint" class="btn btn-default label profile hover-name is-pornstar" data-id="6957567"><span class="model-star-sub icon-f icf-star-o" data-user-id="6957567" data-user-profile="leonie-saint"></span><span class="name">Leonie Saint</span><span class="user-subscribe" data-user-id="6957567" data-user-profile="leonie-saint"><span class="count">12k</span></span></a></li>
        # <li class="model"><a href="/pornstars/abella-danger" class="btn btn-default label profile hover-name is-pornstar" data-id="22053533"><span class="model-star-sub icon-f icf-star-o" data-user-id="22053533" data-user-profile="abella-danger"></span><span class="name">Abella Danger</span><span class="user-subscribe" data-user-id="22053533" data-user-profile="abella-danger"><span class="count">1M</span></span></a></li><li class="model"><a href="/pornstars/adriana-chechik" class="btn btn-default label profile hover-name is-pornstar" data-id="8415660"><span class="model-star-sub icon-f icf-star-o" data-user-id="8415660" data-user-profile="adriana-chechik"></span><span class="name">Adriana Chechik</span><span class="user-subscribe" data-user-id="8415660" data-user-profile="adriana-chechik"><span class="count">857k</span></span></a></li>
        mymatches = re.findall(r'<li(?: class="model"|)><a href="/(amateur-channels|channels|model-channels|models|pornstar-channels|pornstars|profiles)/([a-zA-Z0-9\-\._]+)" class="btn btn-default label profile hover-name(?: is-pornstar|)" data-id="([0-9]+)"><span class="(?:[^"]+)" data-user-id="\3" data-user-profile="([a-zA-Z0-9\-\._]+)"></span><span class="name">([a-zA-Z0-9\-\._\s]+)</span><span class="user-subscribe" data-user-id="\3" data-user-profile="\4"><span class="count">(?:[0-9]+(?:k|M)?)</span></span></a></li>', webpage)
        #print(mymatches)
        # match:1 = type
        # match:2 = name_url
        # match:3 = user_id
        # match:4 = user_profile
        # match:5 = name_txt
        for mymatch in mymatches:
            #print(mymatch)
            #otherprofiles.append(mymatch)
            otherprofiles.append({
                    'type': mymatch[0],
                    'name_url': mymatch[1],
                    'user_id': mymatch[2],
                    'user_profile': mymatch[3],
                    'name_txt': mymatch[4],
                })

        ##IFixThat adding tags (now from @DarkFighterLuke , but going to be changed into my own version later)

        # <meta name="keywords" content="xvideos,xvideos.com, x videos,x video,porn,video,videos,lesbian,teen,hardcore,latina,rough,squirt,big-ass,cheater,twistys,cheat,ass-play,when-girls-play"/>
        tags = self._search_regex(r'<meta name="keywords" content="xvideos,xvideos\.com, x videos,x video,porn,video,videos,(?P<tag>.+?)"', webpage, 'tags', group='tag', default='').split(',')
        if not tags == ['']:
            _ifixthat_print_or_not('tags length > 0')
        else:
            _ifixthat_print_or_not('tags - 0')
            tags = []
        # VS
        # ,"video_tags":["lesbian","teen","hardcore","latina","rough","squirt","big-ass","cheater","twistys","cheat","ass-play","when-girls-play"],
        #tags = []
        #video_meta_matches = re.findall(
        #    r'', webpage)
        #if len(video_meta_matches) > 0:
        #    tags = video_meta_matches[0][0] # transformation needed ?
        #else:
        #    tags = self._search_regex(r'<meta name="keywords" content="xvideos,xvideos\.com, x videos,x video,porn,video,videos,(?P<tag>.+?)"', webpage, 'tags', group='tag', default='').split(',')

        # get tags
        #tags = []
        #mymatches = re.findall(r'<li><a href="/tags/([a-zA-Z0-9\-]+)" class="(is-keyword |)btn btn-default">([a-zA-Z0-9\-]+)</a></li>', webpage)
        #print(mymatches)
        # match:1 = tag_url
        # match:2 = tag_name
        #for mymatch in mymatches:
            #print(mymatch)
            #otherprofiles.append(mymatch)
        #    tags.append({
        #            'tag_url': mymatch[0],
        #            'tag_name': mymatch[2],
        #        })

        ##IFixThat_end

        # pre-fix '<div id="v-views"><span class="icon-f icf-eye"></span>'
        #views = self._search_regex(r'<strong class="mobile-hide">(?P<views>.+?)<', webpage, 'views', group='views', default=None)
        ## VS dirkf
        views = parse_count(get_element_by_class('mobile-hide', get_element_by_id('v-views', webpage)))

        ##IFixThat debug output

        _ifixthat_print_or_not(']]]]]]]]]]]]]]]]]]')
        _ifixthat_print_or_not('title : "%s"' % title)
        _ifixthat_print_or_not('video_id : "%s"' % video_id)
        _ifixthat_print_or_not('ift_idscheme : "%s"' % ift_idscheme)
        _ifixthat_print_or_not('ift_vidid_new : "%s"' % ift_vidid_new)
        _ifixthat_print_or_not('ift_vidid_old : "%s"' % ift_vidid_old)
        _ifixthat_print_or_not('duration : "%s"' % duration)
        _ifixthat_print_or_not('views : "%s"' % views)
        _ifixthat_print_or_not('uploader : "%s"' % uploader)
        _ifixthat_print_or_not('uploader_id : "%s"' % uploader_id)
        _ifixthat_print_or_not('uploader_url : "%s"' % uploader_url)
        _ifixthat_print_or_not('uploader_type : "%s"' % uploader_type)
        _ifixthat_print_or_not('uploader_name_url : "%s"' % uploader_name_url)
        _ifixthat_print_or_not('uploader_name_txt : "%s"' % uploader_name_txt)
        _ifixthat_print_or_not('uploader_name_txt_orig : "%s"' % uploader_name_txt_orig)
        _ifixthat_print_or_not('uploader_user_id : "%s"' % uploader_user_id)
        _ifixthat_print_or_not('uploader_user_profile : "%s"' % uploader_user_profile)
        _ifixthat_print_or_not('otherprofiles : "%s"' % otherprofiles)
        _ifixthat_print_or_not('tags : "%s"' % tags)
        #_ifixthat_print_or_not('xxx : "%s"' % xxx)
        #_ifixthat_print_or_not('xxx : "%s"' % xxx)
        #_ifixthat_print_or_not('xxx : "%s"' % xxx)
        #_ifixthat_print_or_not('xxx : "%s"' % xxx)

        ##IFixThat_end

        return {
            'id': video_id,
            'id_old': ift_vidid_old,
            'id_new': ift_vidid_new,
            'formats': formats,
            'title': title,
            'duration': duration,
            'thumbnails': thumbnails,
            'age_limit': 18,
            'view_count': str_to_int(views),
            'tags': tags,
            'uploader': uploader,
            'uploader_id': uploader_id,
            'uploader_url': uploader_url,
            'uploader_type': uploader_type,
            'uploader_name_url': uploader_name_url,
            'uploader_name_txt': uploader_name_txt,
            'uploader_name_txt_orig': uploader_name_txt_orig,
            'uploader_user_id': uploader_user_id, # same as uploader_id ?
            'uploader_user_profile': uploader_user_profile, # same as uploader_name_url ?
            'otherprofiles': otherprofiles,
        }

#################################################################################################################################################################################### diff-user-types

#class XVideosUserIE(InfoExtractor):

#################################################################################################################################################################################### tag

#class XVideosTagIE(InfoExtractor):

#################################################################################################################################################################################### search

#class XVideosSearchIE(InfoExtractor):




