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
    T,
    traverse_obj,
    try_call,
    txt_or_none,
    join_nonempty,
    LazyList,
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
##IFixThat_end

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

    ##IFixThat TODO=adjust 1)urls 2)info_dict ?)md5
    _TESTS = [{
        'url': 'http://www.xvideos.com/video4588838/biker_takes_his_girl',
        'md5': '14cea69fcb84db54293b1e971466c2e1',
        'info_dict': {
            'id': '4588838',
            'ext': 'mp4',
            'title': 'Biker Takes his Girl',
            'duration': 108,
            'age_limit': 18,
        }
    }, {
        'url': 'https://flashservice.xvideos.com/embedframe/4588838',
        'only_matching': True,
    }, {
        'url': 'http://static-hw.xvideos.com/swf/xv-player.swf?id_video=4588838',
        'only_matching': True,
    }, {
        'url': 'http://xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'https://xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'https://xvideos.es/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'https://www.xvideos.es/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'http://xvideos.es/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'http://www.xvideos.es/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'http://fr.xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'https://fr.xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'http://it.xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'https://it.xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'http://de.xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }, {
        'url': 'https://de.xvideos.com/video4588838/biker_takes_his_girl',
        'only_matching': True
    }]

    ##IFixThat general helper functions (I insert them into every Extractor that I modify - can be removed if not needed)

    def _ifixthat_helper_file_exists(self,filename):
        print('does '+filename+' exist?')
        if os.path.exists(filename):
            print('yes')
            return True
        else:
            print('no')
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
            #print('backing up previous '+filename)
            self._ifixthat_helper_file_archive(filename)
        #print('writing file')
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

    # from dirkf pr
    @classmethod
    def suitable(cls, url):
        EXCLUDE_IE = (XVideosRelatedIE, )
        return (False if any(ie.suitable(url) for ie in EXCLUDE_IE)
                else super(XVideosIE, cls).suitable(url))

    def _real_extract(self, url):
        video_id = self._match_id(url)

        ##IFixThat update initial download to accommodate for old and new ID-scheme

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

        ##IFixThat get for now : old/new ids ++ for later : uploader + tags + actors

## ,"id_video":50011247,"encoded_id_video":"ifbhcpf7201","uploader_id":11422220,"uploader":"twistys1","uploader_url":"\/twistys1","video_tags":["lesbian","teen","hardcore","latina","rough","squirt","big-ass","cheater","twistys","cheat","ass-play","when-girls-play"],"video_models":{"22053533":{"name":"Abella Danger","profile":"abella-danger","uri":"\/pornstars\/abella-danger"},"8415660":{"name":"Adriana Chechik","profile":"adriana-chechik","uri":"\/pornstars\/adriana-chechik"}}}};</script>

##,"id_video":35757155,"encoded_id_video":"iihvcpkf375","uploader_id":24819879,"uploader":"girlswayofficial","uploader_url":"\/girlswayofficial","video_tags":["lesbian","boobs","hot","pornstar","brunette","fingering","squirting","masturbation","pussy-licking","college","facesitting","tribbing","big-tits","nice-ass","romance","girl-on-girl","natural-tits","adriana-chechik","megan-rain"],"video_models":{"8415660":{"name":"Adriana Chechik","profile":"adriana-chechik","uri":"\/pornstars\/adriana-chechik"},"14193845":{"name":"Megan Rain","profile":"megan-rain","uri":"\/pornstars\/megan-rain"}}}};</script>

##,"id_video":1067228,"encoded_id_video":"htuldcb8a9","uploader_id":1705824,"uploader":"","video_tags":[],"video_models":{"6957567":{"name":"Leonie Saint","profile":"leonie-saint","uri":"\/models\/leonie-saint"}}}};</script>

##,"id_video":64065209,"encoded_id_video":"kdhlebvb94e","uploader_id":522199271,"uploader":"sperm-mania","uploader_url":"\/sperm-mania","video_tags":["facial","creampie","shorthair","bukkake","bbw","marie","cumshot-compilation","huge-cumshot","pussy-bukkake","cum-fetish","cum-in-panties","japanese-bukkake","cum-lube","cock-cum","bukkake-compilation"],"video_models":[]}};</script>

#### TO
## ,"id_video":([0-9]+),"encoded_id_video":"([a-z0-9]+)","uploader_id":([0-9]+),"uploader":"([-a-z0-9]+|)",(?:"uploader_url":"\/([-a-z0-9]+)",|)"video_tags":(\[[^]]\]),"video_models":{"22053533":{"name":"Abella Danger","profile":"abella-danger","uri":"\/pornstars\/abella-danger"},"8415660":{"name":"Adriana Chechik","profile":"adriana-chechik","uri":"\/pornstars\/adriana-chechik"}}
        video_meta_matches = re.findall(
            r'"id_video":([0-9]+),"encoded_id_video":"([a-z0-9]+)"', webpage)
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

        ##IFixThat adding contenturl (same as setVideoUrlHigh ?)

        video_url = re.findall(
            r'"contentUrl": "([^"]+)"', webpage)
        #print('video_url')
        #print(video_url)
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

## ,"uploader":"twistys1","uploader_url":"\/twistys1","video_tags":["lesbian","teen","hardcore","latina","rough","squirt","big-ass","cheater","twistys","cheat","ass-play","when-girls-play"],"video_models":{"22053533":{"name":"Abella Danger","profile":"abella-danger","uri":"\/pornstars\/abella-danger"},"8415660":{"name":"Adriana Chechik","profile":"adriana-chechik","uri":"\/pornstars\/adriana-chechik"}}}};

        ##IFixThat adding uploader

        ##IFixThat adding actors

        ##IFixThat adding tags
#<meta name="keywords" content="xvideos,xvideos.com, x videos,x video,porn,video,videos,lesbian,teen,hardcore,latina,rough,squirt,big-ass,cheater,twistys,cheat,ass-play,when-girls-play"/>
#VS
#,"video_tags":["lesbian","teen","hardcore","latina","rough","squirt","big-ass","cheater","twistys","cheat","ass-play","when-girls-play"],


        ##IFixThat_end

########################################
        # get uploader
        uploader_type = ''
        uploader_name_url = ''
        uploader_name_txt = ''
        uploader_name_txt_orig = ''
        uploader_user_id = ''
        uploader_user_profile = ''
        # <li class="main-uploader"><a href="/channels/studio-fow" class="btn btn-default label main uploader-tag hover-name"><span class="name"><span class="icon-f icf-device-tv-v2"></span> Studio Fow</span><span class="user-subscribe" data-user-id="9267136" data-user-profile="studio-fow"><span class="count">308k</span></span></a></li>
        # <li class="main-uploader"><a href="/profiles/hmvthief" class="btn btn-default label main uploader-tag hover-name"><span class="name">Hmvthief</span><span class="user-subscribe" data-user-id="507454529" data-user-profile="hmvthief"><span class="count">2k</span></span></a></li>
        uploader_matches = re.findall(r'<li(?: class="main-uploader"|)><a href="/(amateur-channels|channels|model-channels|models|pornstar-channels|pornstars|profiles)/([a-zA-Z0-9\-\._]+)" class="btn btn-default label main uploader-tag hover-name"><span class="name">(?:<span class="icon-f icf-device-tv-v2"></span> |)([a-zA-Z0-9\-\._\s]+)</span>(?:<span class="icon-f icf-check-circle verified" title="Verified uploader"></span>|)<span class="[a-zA-Z0-9\-\s]*" data-user-id="([0-9]+)" data-user-profile="([a-zA-Z0-9\-\._]+)">', webpage)
        #print(uploader_matches)
        #print(len(uploader_matches))
        if len(uploader_matches) > 0:
            uploader_type = uploader_matches[0][0]
            uploader_name_url = uploader_matches[0][1]
            uploader_name_txt_orig = uploader_matches[0][2]
            # replace " " with "-"
            uploader_name_txt = uploader_name_txt_orig.replace(" ","-")
            uploader_user_id = uploader_matches[0][3]
            uploader_user_profile = uploader_matches[0][4]

        # get all others
        otherprofiles = []
        # <li class="model"><a href="/pornstars/kendra-spade" class="btn btn-default label profile hover-name is-pornstar" data-id="194201359"><span class="name"><span class="icon-f icf-star-o"></span> Kendra Spade</span><span class="user-subscribe" data-user-id="194201359" data-user-profile="kendra-spade"><span class="count">283k</span></span></a></li>
        mymatches = re.findall(r'<li(?: class="model"|)><a href="/(amateur-channels|channels|model-channels|models|pornstar-channels|pornstars|profiles)/([a-zA-Z0-9\-\._]+)" class="btn btn-default label profile hover-name(?: is-pornstar|)" data-id="([0-9]+)"><span class="name">(?:<span class="icon-f icf-star-o"></span> |)([a-zA-Z0-9\-\._\s]+)</span>(?:<span class="icon-f icf-check-circle icf-white-fill verified" title="This profile is verified"></span>|)<span class="[a-zA-Z0-9\-\s]*" data-user-id="([0-9]+)" data-user-profile="([a-zA-Z0-9\-\._]+)">', webpage)
        #print(mymatches)
        # match:1 = type
        # match:2 = name_url
        # match:3 = name_txt
        # match:4 = verified
        # match:5 = user_id
        # match:6 = user_profile
        # match:7 = x
        for mymatch in mymatches:
            #print(mymatch)
            #otherprofiles.append(mymatch)
            otherprofiles.append({
                    'type': mymatch[0],
                    'name_url': mymatch[1],
                    'data_id': mymatch[2],
                    'name_txt': mymatch[3],
                    'user_id': mymatch[4],
                    'user_profile': mymatch[5],
                })
        # get tags
        tags = []
        mymatches = re.findall(r'<li><a href="/tags/([a-zA-Z0-9\-]+)" class="(is-keyword |)btn btn-default">([a-zA-Z0-9\-]+)</a></li>', webpage)
        #print(mymatches)
        # match:1 = tag_url
        # match:2 = tag_name
        for mymatch in mymatches:
            #print(mymatch)
            #otherprofiles.append(mymatch)
            tags.append({
                    'tag_url': mymatch[0],
                    'tag_name': mymatch[2],
                })
########################################

        return {
            'id': video_id,
            'id_old': ift_vidid_old,
            'id_new': ift_vidid_new,
            'formats': formats,
            'title': title,
            'duration': duration,
            'thumbnails': thumbnails,
            'age_limit': 18,
        }
