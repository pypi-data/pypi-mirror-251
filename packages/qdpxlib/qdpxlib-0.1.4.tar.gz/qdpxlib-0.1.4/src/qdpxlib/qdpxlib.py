import json
import numpy as np
import os
import re
import tempfile
from tqdm import tqdm
from uuid import uuid4
import xml.etree.ElementTree as ET
import zipfile


class IntervalManager:
    def __init__(self, file_length):
        self.coded_intervals = []
        self.file_length = file_length
        self.is_sorted = True

    def add_coded_interval(self, start, end):
        self.coded_intervals.append((start, end))
        self.is_sorted = False

    def get_uncoded_intervals(self):
        if not self.is_sorted:
            self.coded_intervals.sort()
            self.is_sorted = True
            
        uncoded_intervals = []
        last_end = 0
        
        for start, end in self.coded_intervals:
            if start > last_end:
                uncoded_intervals.append((last_end, start))
            last_end = max(last_end, end)
        
        if last_end < self.file_length:
            uncoded_intervals.append((last_end, self.file_length))
        
        return uncoded_intervals


class QDPXFile:
    def __init__(
            self, 
            filename, 
            context: int = 100, 
            filter_std: int = 0.5,
            uncoded_word_count_threshold: int = 20,
            default_mean_word_count: int = 7
    ):
        '''
        Initialize the QDPXFile object.
        
        :param filename: The path to the QDPX file.
        :param context: The number of context characters on each side. Default is 100.
        :param filter_std: Number of standard deviations below the mean of the coded data. 
                           Unlabeled sentences with fewer words will be excluded if this is set.
        '''
        self.filename = filename
        self.context = context
        self.filter_std = filter_std
        self.codings = []
        self.codes = {}
        self.code_name_to_guid = {}
        self.uncoded_intervals = {}
        self.default_mean_word_count = default_mean_word_count
        self.uncoded_word_count_threshold = uncoded_word_count_threshold

        self._unzip_qdpx()
        self._parse_qde()

        # Compute statistics for filtering (if applicable)
        if self.filter_std is not None:
            self._compute_statistics()

        self._process_uncoded_intervals()
        self._split_codings_by_sentence()

        # At the end, perform a sanity check
        # self._sanity_check()
        
    def export_qdpx(self, old_qdpx_file, new_qdpx_file):
        '''
        Export modified codings into a new QDPX file.
        
        :param old_qdpx_file: The path to the old QDPX file.
        :param codings: The modified codings.
        :param new_qdpx_file: The path to the new QDPX file to be created.
        '''
        # Extract the old QDPX file to a temporary directory
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(old_qdpx_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        self._clean_file(os.path.join(temp_dir, 'project.qde'))
        
        # Load and modify the project.qde XML file
        tree = ET.parse(os.path.join(temp_dir, 'project.qde'))
        root = tree.getroot()
        xmlns = root.tag[:-7]
        ns = {'qda': 'urn:QDA-XML:project:1.0'}
        
        # Assume the first User is the one who will own new codings
        user_guid = root.find('.//qda:User', namespaces=ns).get('guid')
        
        
        # Remove existing PlainTextSelection elements
        
        for source in root.findall('.//qda:TextSource', namespaces=ns):
            for selection in source.findall('.//qda:PlainTextSelection', namespaces=ns):
                source.remove(selection)
        
        last_idx = {}
        # Insert new codings
        for source_name, _, _, (start_pos, end_pos), labels in tqdm(self.codings):
            source = root.find(f".//qda:TextSource[@guid='{source_name}']", namespaces=ns)
            selection = ET.Element('PlainTextSelection', startPosition=str(start_pos), guid=str(uuid4()), creatingUser=user_guid, modifyingUser=user_guid, endPosition=str(end_pos), name = str(start_pos)+","+str(end_pos))
            
            for label in labels:
                coding = ET.SubElement(selection, 'Coding', guid=str(uuid4()), creatingUser=user_guid)
                ET.SubElement(coding, 'CodeRef', targetGUID=self.code_name_to_guid[label])
            
            if source not in last_idx:
                last_idx[source] = 0
                insert_idx = 0
            else:
                last_idx[source] += 1
                insert_idx = last_idx[source]
            source.insert(insert_idx, selection)
        
    
        
        # Save the modified XML
        ET.indent(tree, space=" ", level=0)
        ET.register_namespace("", "urn:QDA-XML:project:1.0")


        tree.write(os.path.join(temp_dir, 'project.qde'), encoding='utf-8', xml_declaration=True)
        tree.write (os.path.join('../CompareQDPX', 'projecttemp.qde'), encoding='utf-8', xml_declaration=True)
        
        # Create the new QDPX file
        with zipfile.ZipFile(new_qdpx_file, 'w') as new_zip:
            for folder_name, _, filenames in os.walk(temp_dir):
                for filename in filenames:
                    filepath = os.path.join(folder_name, filename)
                    new_zip.write(filepath, os.path.relpath(filepath, temp_dir))


    def _unzip_qdpx(self):
        '''
        Unzip the QDPX file and set the temp_dir.
        '''
        self.temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(self.filename, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

        # Start managing all uncoded intervals
        source_dir = os.path.join(self.temp_dir, 'sources')
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            guid = os.path.splitext(filename)[0]
            with open(file_path, 'r', encoding='utf-8') as f:
                file_length = len(f.read())
            self.uncoded_intervals[guid] = IntervalManager(file_length)


    def _parse_qde(self):
        '''
        Parse the project.qde XML file to extract codes and codings.
        '''
        ns = {'qda': 'urn:QDA-XML:project:1.0'}  # Define the namespace
        self._clean_file(os.path.join(self.temp_dir, 'project.qde'))
        tree = ET.parse(os.path.join(self.temp_dir, 'project.qde'))
        root = tree.getroot()

        # Extract codes
        for code in root.findall('.//qda:Code', namespaces=ns):
            self.codes[code.get('guid')] = code.get('name')
            self.code_name_to_guid[code.get('name')] = code.get('guid')

        # Dictionary to keep track of existing codings
        coding_dict = {}

        # Extract codings
        for source in root.findall('.//qda:TextSource', namespaces=ns):
            source_guid = source.get('guid')
            interval_manager = self.uncoded_intervals[source_guid]
            
            for selection in source.findall('.//qda:PlainTextSelection', namespaces=ns):
                start_pos = int(selection.get('startPosition'))
                end_pos = int(selection.get('endPosition'))

                interval_manager.add_coded_interval(start_pos, end_pos)
                labels_guids = [code.get('targetGUID') for code in selection.findall('.//qda:CodeRef', namespaces=ns)]
                
                # Map GUIDs to their respective labels
                labels = [self.codes.get(guid, "Unknown") for guid in labels_guids]
                
                text_file_path = os.path.join(self.temp_dir, 'sources', f'{source_guid}.txt')
                with open(text_file_path, 'rb') as f:
                    f.seek(start_pos)
                    text_data_bytes = f.read(end_pos - start_pos)
                    text_data = text_data_bytes.decode('utf-8', errors='ignore').strip()
                
                context_before, context_after = self._fetch_context(text_file_path, start_pos, end_pos)
                key = (source_guid, start_pos, end_pos)  # Unique key for each coding
                
                if key in coding_dict:
                    existing_labels = coding_dict[key][-1]
                    existing_labels.extend(labels)
                    existing_labels = list(set(existing_labels))  # Remove duplicates
                    coding_dict[key][-1] = existing_labels
                else:
                    coding_dict[key] = [text_data, (context_before, context_after), labels]

        # Convert the dictionary back to the list format
        self.codings = [
            (key[0], self._clean_text(val[0]), val[1], (key[1], key[2]), val[2])
            for key, val in coding_dict.items()
        ]


    def _split_codings_by_sentence(self, min_sentence_length=10):
        def split_sentence(text):
            # Split the text by .?! and \n
            split_list = re.split(r'([.!?]|\n\n)', text)

            # the regex library splits the delimiters too so we have to 
            # weave them back together
            segments = split_list[::2]
            delimiters = split_list[1::2]
            segments = [seg + delim for seg, delim in zip(segments, delimiters)]

            # If a sentence is too short (ex., "Dr.") we append it to the previous segment
            new_segments = []
            for segment in segments:
                if len(segment) < min_sentence_length:
                    if new_segments:
                        new_segments[-1] += segment
                    else:
                        new_segments.append(segment)
                else:
                    new_segments.append(segment)

            return new_segments
        
        def new_lstrip(text):
            return re.sub(r'^[.!? ]*', '', text)

        def new_strip(text):
            return new_lstrip(text.rstrip())
        
        new_codings = []
        for coding in self.codings:
            sentences = split_sentence(coding[1])
            start_idx = coding[3][0]
            for sentence in sentences:
                # Calculate number of leading and trailing spaces
                leading_spaces = len(sentence) - len(new_lstrip(sentence))
                trailing_spaces = len(sentence) - len(sentence.rstrip())
                
                # Remove leading and trailing spaces
                sentence = new_strip(sentence)
                
                # Compute the length of the sentence (now without leading or trailing spaces)
                sentence_length = len(sentence)
                
                # Compute the indices, adjusting for removed leading spaces
                new_start_idx = start_idx + leading_spaces
                new_end_idx = new_start_idx + sentence_length  # End index is exclusive

                debug_sentence = 'Justin Herring and Justin Bonyoma'
                if debug_sentence in sentence:
                    print('DEBUG')
                    print(coding)
                    print(leading_spaces, trailing_spaces)
                    print(sentence)
                    print(new_start_idx, new_end_idx)
                
                # Replace the sentence in the coding list and append it
                new_coding = [coding[0], sentence, coding[2], (new_start_idx, new_end_idx), coding[4]]
                
                if len(sentence) >= min_sentence_length:
                    new_codings.append(new_coding)
                
                # Adjust indices for the next sentence
                start_idx = new_end_idx + trailing_spaces

        self.codings = new_codings


    def _fetch_context(self, text_file_path, start_pos, end_pos):
        '''
        Fetch context around a coded text.
        
        :param text_file_path: The path to the text source file.
        :param start_pos: The start position of the coded text.
        :param end_pos: The end position of the coded text.
        :returns: A tuple containing the context before and after the coded text.
        '''
        context_before = ''
        context_after = ''
        with open(text_file_path, 'rb') as f:  # Open file in binary mode
            # Fetch context before the coded text
            seek_pos = max(0, start_pos - self.context)
            f.seek(seek_pos)
            context_before_bytes = f.read(start_pos - seek_pos)
            context_before = context_before_bytes.decode('utf-8', errors='ignore').strip()

            # Move to the end of the coded text and fetch context after
            f.seek(end_pos)
            context_after_bytes = f.read(self.context)
            context_after = context_after_bytes.decode('utf-8', errors='ignore').strip()

        context_before = self._clean_text(context_before)
        context_after = self._clean_text(context_after)
        return context_before, context_after


    def _is_valid_uncoded_entry(self, sentence):
        '''
        Filter sentences based on word count and standard deviation.
        
        :param sentences: A list of sentences to be filtered.
        :returns: A filtered list of sentences.
        '''
        if self.uncoded_word_count_threshold:
            threshold = self.uncoded_word_count_threshold
        else:
            threshold = round(self.mean_word_count - (self.filter_std * self.std_word_count))

        return len(sentence.split()) >= threshold


    def _compute_statistics(self):
        '''
        Compute the mean and standard deviation of word count for labeled sentences.
        '''
        # coding[1] is the sentence, coding[-1] is the label.
        # No sentences should have labels when this is called but we use this just in case.
        word_counts = [
            len(coding[1].split()) # number of words
            for coding in self.codings 
            if coding[-1] # if the sentence is coded
        ]

        # if we are doing inference and there are no labels, set stats to some default
        if not word_counts:
            word_counts = [self.default_mean_word_count]

        self.mean_word_count = np.mean(word_counts)
        self.std_word_count = np.std(word_counts)


    def _process_uncoded_intervals(self):
        '''
        Process the uncoded intervals and update self.codings.
        '''
        for source_guid, interval_manager in self.uncoded_intervals.items():
            text_file_path = os.path.join(self.temp_dir, f'sources/{source_guid}.txt')
            uncoded_intervals = interval_manager.get_uncoded_intervals()
            
            for start_pos, end_pos in uncoded_intervals:
                with open(text_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    f.seek(start_pos)
                    text_segment = f.read(end_pos - start_pos)
                    text_segment = self._clean_text(text_segment)
                
                sentences = text_segment.split('\n\n')

                # Initialize running_pos to the start of the current interval
                running_pos = start_pos
                
                for sentence in sentences:
                    sentence_start_pos = running_pos
                    sentence_end_pos = running_pos + len(sentence)
                    
                    context_before, context_after = self._fetch_context(text_file_path, sentence_start_pos, sentence_end_pos)

                    if self._is_valid_uncoded_entry(sentence):
                        self.codings.append(
                            (source_guid, sentence, (context_before, context_after), (sentence_start_pos, sentence_end_pos), [])
                        )
                    
                    # +2 to account for the two newline characters used for splitting
                    running_pos += len(sentence) + 2


    def _clean_text(self, text):
        '''
        Remove all non-ascii characters from text.
        '''
        return ''.join(char if ord(char) < 128 else ' ' for char in text)
    

    def _clean_file(self, filename):
        '''
        Remove all non-ascii characters from a file.
        '''
        string = open(filename).read()
        new_str = ''.join([c for c in string if ord(c) in range(32, 127)])
        open(filename, 'w').write(new_str)


    def _sanity_check(self):
        '''
        Sanity check on self.codings
        '''
        print('Performing a sanity check...')
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(self.filename, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for coding in self.codings:
            guid, text, _, (start, end), _ = coding
            if len(text) != (end - start):
                print(f'SANITY CHECK FAILED ON SENTENCE: {text} (INDICES {start}-{end})')
                print(len(text), end-start)

            with open(os.path.join(temp_dir, 'sources', f'{guid}.txt')) as f:
                doc = f.read()
                if doc.find(text) != start:
                    print('SANITY CHECK FAILED:')
                    print('\tIndex in document:', doc.find(text))
                    print('\tIndex given:', start)
                    print(text)
                    exit(0)


if __name__ == '__main__':
    qdpx_file = os.path.join(
        '..',
        'data',
        '2023-10-20 MasterTraining File.qdpx'
    )
    output_json = 'master_dataset.json'
    output_qdpx = 'tempQDPX.qdpx'

    qdpx = QDPXFile(qdpx_file)

    # Export them as JSON
    print('Exporting JSON')
    with open(output_json, 'w') as f:
        json.dump(qdpx.codings, f, indent=4)
    print('Exported JSON')

    # Export new qdpx file
    print('Exporting new QDPX')
    with open(output_qdpx, 'wb') as f:
        qdpx.export_qdpx(qdpx_file, f)
    print('Exported new QDPX')