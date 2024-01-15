"""
-------------------------------
The data_query module
-------------------------------
This module defines two classes that allow to parse author data from
Orcid and arxiv.
These are AuthorData and OrcidWork.
"""

from __future__ import annotations
from urllib import request, parse
import logging
import json
import os

from .abstract_collector import main_paragraph
import feedparser
from rapidfuzz.distance import DamerauLevenshtein


from .user_config import orcid_token


class AuthorData:
    """A class to parse Orcid author entries."""

    def __init__(self, orcid_id: str):
        """Instantiator

        Args:
            orcid_id (str): The author's orcid id
        """
        self.orcid_id = orcid_id
        self._orcid_record = None
        self._arxiv_record = None
        self._orcid_id_is_on_arxiv = None
        self._arxiv_summaries_dic = None

    def _set_orcid_record(self):
        headers = {}
        headers["Authorization"] = "Bearer %s" % orcid_token
        headers["Accept"] = "application/json"
        url = "https://pub.orcid.org/v2.0/%s/works" % self.orcid_id
        my_request = request.Request(url, headers=headers)
        response = request.urlopen(my_request)
        loaded = json.load(response)
        self._orcid_record = loaded

    def _set_arxiv_record(self):
        url = "https://arxiv.org/a/%s.atom" % self.orcid_id
        my_request = request.Request(url)
        try:
            response = request.urlopen(my_request)
            self._arxiv_record = response
            self._orcid_id_is_on_arxiv = True

        except:
            self._orcid_id_is_on_arxiv = False
            self._arxiv_record = ""

    @property
    def orcid_record(self) -> list:
        """The raw orcid record as a parsed json.

        Returns:
            list: The raw orcid record as a parsed json (using json.load).
        """
        if self._orcid_record is None:
            self._set_orcid_record()

        return self._orcid_record

    @property
    def arxiv_record(self) -> list:
        """The raw arxiv record as an atom feed."""
        if self._arxiv_record is None:
            self._set_arxiv_record()

        return self._arxiv_record

    @property
    def articles(self) -> list[OrcidWork]:
        """list of article entries in the author's Orcid entry.

        Returns:
            list[OrcidWork]: list of article entries, formatted as OrcidWork instances.
        """
        articles_list = []
        for item in self.orcid_record["group"]:
            if item["work-summary"][0]["type"] == "JOURNAL_ARTICLE":
                articles_list.append(OrcidWork(item))
        return articles_list

    @property
    def orcid_id_is_on_arxiv(self) -> bool:
        """Check if the author associated his/her Arxiv  with Orcid.

        Returns:
            bool: True if yes, False if no!
        """
        if self._orcid_id_is_on_arxiv is None:
            self._set_arxiv_record()
        return self._orcid_id_is_on_arxiv

    def _set_arxiv_summaries_dic(self):
        d = feedparser.parse(self.arxiv_record)
        # below, we reset _arxiv_record to None because it was destroyed by
        # feedparser.parse
        self._arxiv_record = None
        dic = {entry.title: entry.summary for entry in d.entries}
        self._arxiv_summaries_dic = dic

    @property
    def arxiv_summaries_dic(self) -> dict:
        """Return dict that maps arxiv_entries -> abstracts for the author."""
        if self._arxiv_summaries_dic is None:
            self._set_arxiv_summaries_dic()
        return self._arxiv_summaries_dic

    def work_summary_from_arxiv(self, orcid_work: OrcidWork) -> str:
        """Match work with an arxiv entry to provide a summary.

        Args:
            orcid_work (OrcidWork): the work that needs summary.

        Returns:
            str: The guessed summary
        """
        dic_arxiv = self.arxiv_summaries_dic
        if orcid_work.title in dic_arxiv:
            logging.info(
                "Abstract for %s found through a perfect title match on the arxiv."
                % orcid_work.title
            )
            return dic_arxiv[orcid_work.title].replace("\n", "")
        else:
            keys = list(dic_arxiv.keys())
            keys.sort(
                key=lambda s: DamerauLevenshtein.normalized_similarity(
                    s.lower(), orcid_work.title.lower()
                )
            )
            best_key = keys[-1]
            logging.warning(
                "We used string similarity to find the summary of %s."
                % orcid_work.title
                + "We used the summary of the arxiv entry %s " % best_key
                + ". Please check this is a correct choice."
            )
            return dic_arxiv[best_key]


class OrcidWork:
    def __init__(self, work_data):
        """Instantiate single work object.

        Args:
            work_data (nested lists/dictionaries): part of a loaded json
             data corresponding to a single work, as obtained from orcid's
             API.
        """
        self.raw_data = work_data
        self._doi = None
        self._doi_bibtex = None
        self._orcid_bibtex = None

    @property
    def path(self):
        "Orcid path to the data."
        return self.raw_data["work-summary"][0]["path"]

    @property
    def title(self):
        """Work title."""
        return self.raw_data["work-summary"][0]["title"]["title"]["value"]

    def _set_doi(self):
        ids = self.raw_data["work-summary"][0]["external-ids"]["external-id"]
        for entry in ids:
            if (
                entry["external-id-relationship"] == "SELF"
                and entry["external-id-type"] == "doi"
            ):
                self._doi = entry["external-id-value"]
                break
        if self._doi is None:
            raise KeyError(
                "No entry found in the orcid record to provide the doi of the article."
            )

    @property
    def doi(self) -> str:
        """The Work's doi.

        Returns:
            str: the doi.
        """
        if self._doi is None:
            self._set_doi()
        return self._doi

    @property
    def url_in_journal(self):
        return "https://doi.org/%s" % self.doi

    def _set_bibtex_from_doi(self):
        headers = {}
        headers["Accept"] = "text/bibliography; style=bibtex"
        my_request = request.Request(self.url_in_journal, headers=headers)
        response = request.urlopen(my_request)
        self._doi_bibtex = response.read().decode("utf-8")

    # We are not sure the method below gets any extra info on the work.
    def _work_details(self):
        headers = {}
        headers["Authorization"] = "Bearer %s" % orcid_token
        headers["Accept"] = "application/json"
        url = "https://pub.orcid.org/v2.0%s" % self._path
        my_request = request.Request(url, headers=headers)
        response = request.urlopen(my_request)
        loaded = json.load(response)
        return loaded

    @property
    def bibtex(self, source: str = "doi"):
        """Return the bibtex entry for self from source.

        Args:
            source (str, optional): Equals 'doi'. Defaults to 'doi'.
            Other sources might be available in the future.
        """
        if source == "doi":
            if self._doi_bibtex is None:
                self._set_bibtex_from_doi()
            return self._doi_bibtex
        else:
            raise ValueError(
                "Currently, the only admissible value for the source parameter is 'doi'."
            )

    def scrape_abstract(self):
        """Scrape the work's summary from the editor/journal's site.
        Beware that you might need authorization from the editor/journal to use this functionality.
        """
        url = "https://doi.org/%s" % self.doi
        main_par = main_paragraph(url)
        logging.warning(
            "We got the abstract for %s scraping the editor/journal's website."
            % self.title
            + "Make sure the result is satisfactory and beware that you might need "
            "authorization from the editor/journal to use this functionality."
        )
