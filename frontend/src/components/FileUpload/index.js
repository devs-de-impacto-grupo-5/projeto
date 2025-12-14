import { useState } from 'react';
import { Container, UploadButton, HiddenInput, FileName, SendButton } from './style';
import { FiUpload, FiSend } from 'react-icons/fi';

const FileUpload = ({ onFileSelect }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSend = () => {
    if (selectedFile && onFileSelect) {
      onFileSelect(selectedFile);
      setSelectedFile(null);
    }
  };

  return (
    <Container>
      <HiddenInput
        type="file"
        id="file-upload"
        accept=".pdf,.jpg,.jpeg,.png"
        onChange={handleFileChange}
      />
      <UploadButton as="label" htmlFor="file-upload">
        <FiUpload size={20} />
        {selectedFile ? 'Trocar arquivo' : 'Escolher arquivo'}
      </UploadButton>

      {selectedFile && (
        <>
          <FileName>{selectedFile.name}</FileName>
          <SendButton onClick={handleSend}>
            <FiSend size={20} />
            Enviar
          </SendButton>
        </>
      )}
    </Container>
  );
};

export default FileUpload;
